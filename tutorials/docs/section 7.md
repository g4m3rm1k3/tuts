# PDM Tutorial - Stage 7: Version Control with Git Integration

**Prerequisites**: Completed Stage 6. Your app should enforce ownership (only checkin your locks), log audits on all actions, and show admin panel/logs. Test: Login as john, checkout file—can't checkin as admin (error), admin force works + logs.
**Time**: 5-6 hours
**What you'll build**: Git commits on checkin (with message), history viewing (commits list), diffs (change view), rollback (admin revert). _Incremental_: One Git method/UI element at a time, test with curl/console. **Tailwind**: Yes—history modal with `max-h-96 overflow-y-auto flex flex-col gap-3`, commit items as `p-4 border-l-4 border-primary rounded bg-secondary`.

---

### Deep Dive - Git Internals (CS: Content Addressing, SE: Versioned Data)

**CS Topic**: Git = content-addressable store (CS: Merkle tree—hash(content) = unique ID, tamper-proof chain). Commits = snapshots (full files, not deltas, CS: immutability for branching). **App Topic**: Commit on checkin = audit + revert (ties to Stage 6 logs). **SE Principle**: Version everything (reproducible builds, rollback bugs). **Python Specific**: GitPython = lib wrapper (git CLI under hood, safe from shell injection). **JS Specific**: No Git in browser—API for history (fetch chain). Gotcha: Commits = O(1) append, but push/pull = network (async).

Run your `learn_git_internals.py` if created—demo shows hash same content = same ID (dedup).

---

### 7.1: Install GitPython (One Dep)

**Step 1: Add to requirements.txt**

```
gitpython==3.1.40  # NEW: Git ops
```

```bash
pip install -r requirements.txt
```

- **Explanation**: GitPython = Python Git (CS: binding, Repo = graph walker). 3.1.40 = stable (SE: pinned).
- **Test**: `python -c "import git; print('OK')"` → OK.
- **Gotcha**: Requires system Git (git --version >2.30).

---

### 7.2: Update Configuration (One Git Path)

**Step 1: Add Git Path**
In `config.py` Settings:

```python
GIT_REPO_PATH: Path = BASE_DIR / "git_repo"  # NEW: Git storage
```

- **Explanation**: Separate from repo/ (working files)—Git tracks versions (app: snapshot vs live).
- **Test**: Restart server—no crash. Shell: `python -c "from app.config import settings; print(settings.GIT_REPO_PATH)"` → /path/git_repo.
- **Gotcha**: BASE_DIR = parent (Stage 0 structure).

---

### 7.3: Git Service Layer (Build GitService Incremental)

**Step 1: Create git_service.py**

```bash
mkdir -p backend/app/services  # If missing
touch backend/app/services/git_service.py
```

Paste skeleton:

```python
import git  # NEW: Lib
from pathlib import Path  # NEW
from typing import List, Dict, Optional  # NEW
import logging  # NEW
from datetime import datetime, timezone  # NEW
from app.config import settings  # NEW

logger = logging.getLogger(__name__)

class GitService:  # NEW
    def __init__(self, repo_path: Path):
        self.repo_path = repo_path
        self.repo = None
        self._ensure_repo()  # Stub
```

- **Explanation**: GitService = VCS facade (SE: abstraction). \_ensure = private (convention).
- **Test**: `python -c "from app.services.git_service import GitService; GitService(Path('test'))"` → OK.
- **Gotcha**: Import git = CLI dep (install Git).

**Step 2: Add \_ensure_repo (Init/Open)**
Add:

```python
    def _ensure_repo(self):  # NEW
        try:
            self.repo = git.Repo(self.repo_path)  # NEW: Open
            logger.info(f"Opened Git repo at {self.repo_path}")
        except (git.InvalidGitRepositoryError, Exception):  # NEW
            logger.info(f"Creating Git repo at {self.repo_path}")
            self.repo_path.mkdir(parents=True, exist_ok=True)
            self.repo = git.Repo.init(self.repo_path)  # NEW: Init
```

- **Explanation**: Except broad = handle all (CS: exception hierarchy). init = empty .git/.
- **Test**: Call \_ensure_repo—creates .git if missing.
- **Gotcha**: InvalidGitRepositoryError = no .git.

**Step 3: Add Config (User)**
Add in except:

```python
            with self.repo.config_writer() as config:  # NEW
                config.set_value("user", "name", settings.GIT_USER_NAME)  # NEW
                config.set_value("user", "email", settings.GIT_USER_EMAIL)
```

- **Explanation**: config_writer = transaction (CS: atomic config). User = commit author.
- **Test**: `git config --get user.name` in git_repo → "PDM System".
- **Gotcha**: Add GIT_USER_NAME/EMAIL to config.py if missing (from Stage 2).

**Step 4: Add Initial Commit**
Add after config:

```python
            readme_path = self.repo_path / "README.md"  # NEW
            readme_path.write_text("## PDM Git Repo\nVersioned files.")  # NEW
            self.repo.index.add(["README.md"])  # NEW: Stage
            self.repo.index.commit("Initial commit")  # NEW: Commit
            logger.info("Initial commit created")
```

- **Explanation**: Index = staging (CS: pending set). Commit = snapshot.
- **Test**: `cd backend/git_repo && git log --oneline` → "Initial commit".
- **Gotcha**: Add all or specific (here one file).

**Step 5: Add add_file (Stage)**
Add:

```python
    def add_file(self, filename: str, content: bytes):  # NEW
        file_path = self.repo_path / filename
        file_path.write_bytes(content)
        logger.info(f"Added to Git: {filename}")
```

- **Explanation**: write_bytes = binary (app: .mcam).
- **Test**: add_file("test.txt", b"test")—file created.

**Step 6: Add commit_file (Full Commit)**
Add:

```python
    def commit_file(self, filename: str, message: str, author_name: str, author_email: Optional[str] = None) -> str:  # NEW
        if not self.file_exists(filename):  # NEW
            raise ValueError(f"No file: {filename}")
        try:
            self.repo.index.add([filename])  # NEW
            author_email = author_email or f"{author_name}@pdm.local"
            commit = self.repo.index.commit(  # NEW
                message,
                author=f"{author_name} <{author_email}>",
                author_date=datetime.now(timezone.utc).isoformat(),
                commit_date=datetime.now(timezone.utc).isoformat()
            )
            logger.info(f"Committed {filename}: {commit.hexsha[:8]}")
            return commit.hexsha
        except git.exc.GitCommandError as e:
            logger.error(f"Commit failed: {e}")
            raise ValueError(f"Commit failed: {e}")
```

- **Explanation**: hexsha = hash str (CS: content address). Author = metadata.
- **Test**: add_file, commit_file—git log shows commit.
- **Gotcha**: CommandError = git fail (e.g., no changes).

**Step 7: Add get_file_history (Log)**
Add:

```python
    def get_file_history(self, filename: str, limit: int = 50) -> List[Dict]:  # NEW
        try:
            commits = []
            for commit in self.repo.iter_commits(paths=filename, max_count=limit):  # NEW: Iter
                commits.append({
                    'sha': commit.hexsha,
                    'short_sha': commit.hexsha[:8],
                    'message': commit.message.strip(),
                    'author': commit.author.name,
                    'date': commit.committed_datetime.isoformat(),
                    'timestamp': commit.committed_date,
                })
            return commits
        except git.exc.GitCommandError as e:
            logger.error(f"History failed: {e}")
            return []
```

- **Explanation**: iter_commits = generator (CS: lazy). paths = filter (efficient).
- **Test**: Commit twice, get_history → List of 2.
- **Gotcha**: max_count = limit (perf).

**Step 8: Add get_file_diff**
Add:

```python
    def get_file_diff(self, filename: str, commit_sha: str) -> Dict:  # NEW
        try:
            commit = self.repo.commit(commit_sha)
            if not commit.parents:  # NEW: Initial
                return {'type': 'added', 'content': self._get_file_at_commit(filename, commit_sha), 'diff': None}
            parent = commit.parents[0]
            diffs = parent.diff(commit, paths=filename, create_patch=True)  # NEW
            if not diffs:
                return {'type': 'unchanged', 'diff': None}
            diff = diffs[0]
            return {
                'type': 'modified' if diff.a_path else 'added',
                'old_content': diff.a_blob.data_stream.read().decode('utf-8', errors='ignore') if diff.a_blob else None,
                'new_content': diff.b_blob.data_stream.read().decode('utf-8', errors='ignore') if diff.b_blob else None,
                'diff': diff.diff.decode('utf-8', errors='ignore'),
            }
        except Exception as e:
            logger.error(f"Diff failed: {e}")
            return {'type': 'error', 'error': str(e)}
    def _get_file_at_commit(self, filename: str, commit_sha: str) -> str:  # NEW private
        commit = self.repo.commit(commit_sha)
        blob = commit.tree / filename
        return blob.data_stream.read().decode('utf-8', errors='ignore')
```

- **Explanation**: diff = patch (CS: unified format). data_stream = lazy read (perf).
- **Test**: Diff commit—returns {'diff': '--- +added line'}.
- **Gotcha**: decode errors='ignore' = robust.

**Step 9: Add rollback_file**
Add:

```python
    def rollback_file(self, filename: str, commit_sha: str) -> str:  # NEW
        try:
            commit = self.repo.commit(commit_sha)
            blob = commit.tree / filename
            old_content = blob.data_stream.read()
            file_path = self.repo_path / filename
            file_path.write_bytes(old_content)
            self.repo.index.add([filename])
            rollback_commit = self.repo.index.commit(f"Rollback {filename} to {commit_sha[:8]}")
            logger.info(f"Rolled back {filename}")
            return rollback_commit.hexsha
        except Exception as e:
            logger.error(f"Rollback failed: {e}")
            raise ValueError(f"Rollback failed: {e}")
```

- **Explanation**: Checkout to old (immutable new commit, CS: no history rewrite).
- **Test**: Rollback—new commit with old content.
- **Gotcha**: write_bytes = overwrite working.

**Full git_service.py** (End of Section—Verify):
[Full with all methods]

**Verification**: Commit, history → Commits. Diff → Patch. Rollback → New commit old file.

### 7.4: Integrate Git with FileService (Hooks Incremental)

**Step 1: Update FileService **init****
Add git_repo_path param:

```python
def __init__(self, repo_path: Path, locks_file: Path, audit_file: Path, git_repo_path: Path):  # NEW
    # ... existing
    self.git_service = GitService(git_repo_path)  # NEW
```

- **Explanation**: Inject Git (SE: DI).
- **Test**: Init with path—OK.

**Step 2: Hook checkout_file (Initial Copy)**
In checkout_file after acquire_lock:

```python
if not self.git_service.file_exists(filename):  # NEW
    content = self.repository.read_file(filename)
    self.git_service.add_file(filename, content)
    self.git_service.commit_file(filename, f"Initial version of {filename}", user)
```

- **Explanation**: Lazy init (first checkout commits baseline).
- **Test**: Checkout new file—git_repo/test.mcam + commit.

**Step 3: Hook checkin_file (Commit Changes)**
In checkin_file after release_lock:

```python
content = self.repository.read_file(filename)  # NEW
self.git_service.add_file(filename, content)
commit_message = lock_info.get('message', 'Updated') if lock_info else 'Updated'  # NEW
commit_sha = self.git_service.commit_file(filename, f"Checkin: {commit_message}", user)  # NEW
self.audit_logger.log_action('checkin', filename, user, {'commit_sha': commit_sha})
```

- **Explanation**: Commit message from lock (app: traceable). Audit SHA (immutable link).
- **Test**: Checkin—git log shows "Checkin: ...".

**Full FileService** (End of Section—Verify):
[Full with Git hooks]

**Verification**: Checkin → Git commit + audit SHA.

### 7.5: Version Control API Endpoints (Routes Incremental)

**Step 1: Create version_control.py**

```bash
touch backend/app/api/version_control.py
```

Paste:

```python
from fastapi import APIRouter  # NEW
from typing import List  # NEW
from app.services.file_service import FileService  # NEW
from app.api.deps import get_file_service, get_current_user  # NEW
from app.schemas.auth import User  # NEW

router = APIRouter(prefix="/api/version-control", tags=["version-control"])
```

- **Test**: Import OK.

**Step 2: Add /history/{filename}**
Add:

```python
@router.get("/{filename}/history")  # NEW
def get_file_history(
    filename: str,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    file_service: FileService = Depends(get_file_service)
):
    try:
        history = file_service.get_file_history(filename, limit)
        return {"filename": filename, "commits": history, "count": len(history)}
    except Exception as e:
        raise HTTPException(500, f"History failed: {str(e)}")
```

- **Import**: `from fastapi import HTTPException, status; from typing import Optional`.
- **Test**: /docs, call /api/version-control/test.mcam/history → Empty commits.

**Step 3: Add /diff/{filename}/{commit_sha}**
Add:

```python
@router.get("/diff/{filename}/{commit_sha}")  # NEW
def get_file_diff(
    filename: str,
    commit_sha: str,
    current_user: User = Depends(get_current_user),
    file_service: FileService = Depends(get_file_service)
):
    try:
        diff = file_service.get_file_diff(filename, commit_sha)
        return {"filename": filename, "commit_sha": commit_sha, "diff": diff}
    except Exception as e:
        raise HTTPException(500, f"Diff failed: {str(e)}")
```

- **Test**: After commit, call → Diff dict.

**Step 4: Add /rollback (Admin)**
Add:

```python
from app.api.deps import require_admin  # NEW

@router.post("/rollback/{filename}/{commit_sha}")  # NEW
def rollback_file(
    filename: str,
    commit_sha: str,
    current_user: User = Depends(require_admin),
    file_service: FileService = Depends(get_file_service)
):
    try:
        new_commit = file_service.rollback_file(filename, commit_sha, current_user.username)
        return {"success": True, "message": f"Rolled back to {commit_sha[:8]}", "new_commit": new_commit}
    except ValueError as e:
        raise HTTPException(403, str(e))
```

- **Test**: As admin POST → Success.

**Step 5: Include in main.py**
Add:

```python
from app.api import files, auth, version_control  # NEW
app.include_router(version_control.router)
```

- **Test**: /docs → Version-control tag.

**Full version_control.py** (End of Section—Verify):

```python
from fastapi import APIRouter, HTTPException, status, Depends
from typing import List, Optional
from app.services.file_service import FileService
from app.api.deps import get_file_service, get_current_user, require_admin
from app.schemas.auth import User

router = APIRouter(prefix="/api/version-control", tags=["version-control"])

@router.get("/{filename}/history")
def get_file_history(
    filename: str,
    limit: int = 50,
    current_user: User = Depends(get_current_user),
    file_service: FileService = Depends(get_file_service)
):
    try:
        history = file_service.get_file_history(filename, limit)
        return {"filename": filename, "commits": history, "count": len(history)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"History failed: {str(e)}")

@router.get("/diff/{filename}/{commit_sha}")
def get_file_diff(
    filename: str,
    commit_sha: str,
    current_user: User = Depends(get_current_user),
    file_service: FileService = Depends(get_file_service)
):
    try:
        diff = file_service.get_file_diff(filename, commit_sha)
        return {"filename": filename, "commit_sha": commit_sha, "diff": diff}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Diff failed: {str(e)}")

@router.post("/rollback/{filename}/{commit_sha}")
def rollback_file(
    filename: str,
    commit_sha: str,
    current_user: User = Depends(require_admin),
    file_service: FileService = Depends(get_file_service)
):
    try:
        new_commit = file_service.rollback_file(filename, commit_sha, current_user.username)
        return {"success": True, "message": f"Rolled back to {commit_sha[:8]}", "new_commit": new_commit}
    except ValueError as e:
        raise HTTPException(status_code=403, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Rollback failed: {str(e)}")
```

**Verification**: /api/version-control/test.mcam/history → Commits. POST rollback as admin → Success.

### 7.6: Frontend - History Modal & Rollback (Tailwind Incremental)

**Step 1: Add History Modal to index.html**
Before </body>:

```html
<div id="history-modal" class="modal-overlay hidden">
  # NEW
  <div class="modal-content max-w-4xl">
    # Tailwind wide
    <div class="modal-header">
      <h3>History: <span id="history-filename"></span></h3>
      <button class="modal-close">&times;</button>
    </div>
    <div class="modal-body">
      <div
        id="history-list"
        class="flex flex-col gap-3 max-h-96 overflow-y-auto"
      ></div>
      # NEW
    </div>
  </div>
</div>
```

- **Explanation**: max-w-4xl = wide (Tailwind arbitrary). gap-3 = spacing.
- **Test**: .open class—modal scrolls.

**Step 2: Add History Button in createFileElement**
In actionsDiv (after checkin if checked_out):

```javascript
const historyBtn = document.createElement("button");  # NEW
historyBtn.className = "btn btn-info btn-sm";  # NEW Tailwind
historyBtn.textContent = "History";
historyBtn.onclick = (e) => { e.stopPropagation(); handleHistory(file.name); };  # NEW
actionsDiv.appendChild(historyBtn);
```

- **Add to input.css @layer components**: `.btn-info { @apply bg-info text-inverse; } .btn-info:hover { @apply bg-info-dark; }` (define info-dark in config).
- **Explanation**: stopPropagation = event bubbling stop (CS: event phase). btn-info = semantic.
- **Test**: Button shows, click calls stub.

**Step 3: Add handleHistory & loadHistory in app.js**
Add:

```javascript
async function handleHistory(filename) {  # NEW
  document.getElementById("history-filename").textContent = filename;
  historyModal.open();  # Assume instance
  await loadHistory(filename);
}
async function loadHistory(filename) {  # NEW
  const container = document.getElementById("history-list");
  container.innerHTML = '<div class="text-center py-8 text-secondary">Loading...</div>';  # Tailwind
  try {
    const data = await apiClient.getFileHistory(filename);  # NEW
    if (data.commits.length === 0) {
      container.innerHTML = '<div class="text-center py-8 text-secondary">No history.</div>';
      return;
    }
    container.innerHTML = data.commits.map((commit) => createCommitElement(commit, filename)).join("");
  } catch (error) {
    container.innerHTML = `<div class="text-center py-8 text-danger">Error: ${error.message}</div>`;
  }
}
```

- **Add to api-client.js**:
  ```javascript
  async getFileHistory(filename, limit = 50) {
    return this.get(`/api/version-control/history/${encodeURIComponent(filename)}?limit=${limit}`);
  }
  ```
- **Explanation**: Await chain = sequential (CS: promise resolve). Map/join = render (functional).
- **Test**: Click History—loading, then commits or "No history".
- **Gotcha**: encodeURIComponent = URL safe.

**Step 4: Add createCommitElement**
Add:

```javascript
function createCommitElement(commit, filename) {  # NEW
  const date = new Date(commit.date);
  const role = localStorage.getItem("user_role");
  return `
    <div class="commit-item p-4 border border-default border-l-4 border-primary rounded-md bg-secondary mb-3 transition-all hover:-translate-x-1 hover:shadow-sm">
      <div class="flex justify-between items-start mb-2">
        <div class="font-semibold text-primary mb-1">${commit.message}</div>
        <div class="text-sm text-secondary">${date.toLocaleString()}</div>
      </div>
      <div class="text-xs text-secondary flex gap-4">
        <span>👤 ${commit.author}</span>
        <code class="bg-tertiary px-2 py-1 rounded text-xs">${commit.short_sha}</code>
      </div>
      <div class="flex gap-2 mt-3">
        <button class="btn btn-secondary btn-sm" onclick="viewDiff('${filename}', '${commit.sha}')">View Diff</button>
        ${role === "admin" ? `<button class="btn btn-warning btn-sm" onclick="rollbackTo('${commit.sha}')">Rollback</button>` : ''}
      </div>
    </div>
  `;
}
```

- **Explanation**: Tailwind = pretty (p-4 = padding, hover:-translate-x-1 = lift). Template literal = embed (JS: string interp).
- **Test**: Load—styled commits with buttons.
- **Gotcha**: onclick = global (add event listeners for complex).

**Step 5: Add viewDiff & rollbackTo**
Add:

```javascript
async function viewDiff(filename, sha) {  # NEW
  // Stub modal or console.log(`Diff ${filename} at ${sha}`)
  console.log(`Diff for ${filename} at ${sha}`);  # Temp
}
async function rollbackTo(sha) {  # NEW
  if (!confirm(`Rollback to ${sha.slice(0,7)}?`)) return;
  try {
    await apiClient.rollbackFile(currentHistoryFile, sha);  # NEW
    toast.success("Rolled back!");
    historyModal.close();
    loadFiles();
  } catch (error) {
    toast.error(error.message);
  }
}
```

- **Add to api-client.js**:
  ```javascript
  async getFileDiff(filename, commitSha) { return this.get(`/api/version-control/diff/${encodeURIComponent(filename)}/${commitSha}`); }
  async rollbackFile(filename, commitSha) { return this.post(`/api/version-control/rollback/${encodeURIComponent(filename)}/${commitSha}`); }
  ```
- **Explanation**: Confirm = UX gate (SE: confirmation for destructive). slice = short SHA.
- **Test**: Click View—console. Rollback—POST, toast.

**Step 6: Add historyModal Instance**
In DOMContentLoaded:

```javascript
const historyModal = new ModalManager("history-modal");  # NEW
```

- **Explanation**: Instance = reusable (revisit Stage 3 modals).
- **Test**: Click History—modal opens.

**Full app.js** (End of Section—Verify):
[Full with history functions, Tailwind in templates]

**Verification**: History button → Modal with styled commits, diff/rollback buttons work.

### Stage 7 Complete

**Test Full**: Checkin → Git commit. History → List/diff. Admin rollback → Reverts.

**Verification**:

- [ ] Commits on checkin.
- [ ] History modal pretty (Tailwind).
- [ ] Diff console (add modal later if needed).
- [ ] Rollback success.

**What You Learned (Depth)**:

- **CS**: Merkle (hash chain), iterators (iter_commits).
- **App**: Hooks (checkout → initial commit).
- **Python**: GitPython (Repo.index).
- **JS**: Template literals (render).
- **SE**: Immutable commits (no rewrite).

Ready for Stage 8 (Hybrid GitLab)?
