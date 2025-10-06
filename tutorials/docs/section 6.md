# PDM Tutorial - Stage 6: Advanced Authorization & Audit System

**Prerequisites**: Completed Stage 5. Your app should require login for /api/files, return 401 without token, and create defaults (admin/john). Test: Login via /login, /api/files with Bearer token → Files list.
**Time**: 4-5 hours
**What you'll build**: Ownership validation (only checkin your locks), audit logging (JSON trail), admin-only endpoints (force checkin, logs), frontend admin panel/modal. _Incremental_: One validation/log per step, test with curl/UI. **Tailwind**: Yes—admin panel as `bg-warning/10 border-warning p-6 rounded-lg`, audit modal with `max-h-96 overflow-y-auto`.

---

### Deep Dive: Authorization Patterns (CS: ACL/RBAC, SE: Logging)

**CS Topic**: AuthZ = policy enforcement (CS: access control lists = per-resource perms, RBAC = role groups). Ownership = resource-based (CS: graph where user owns node). Audit = immutable log (CS: append-only ledger like blockchain, tamper-evident). **App Topic**: Force checkin = admin escape hatch (UX: recovery without data loss). **SE Principle**: Audit everything (compliance, debug—OWASP logging). **Python Specific**: Decorator factories (require_role = higher-order). **JS Specific**: Confirm dialogs for destructive (user consent). Gotcha: Logs = performance (async later).

Create `backend/app/learn_authorization.py` (paste your original)—run `python -m app.learn_authorization` to see RBAC/ABAC demo.

---

### 6.1: Enhanced Lock Management with Ownership (Refactor LockManager Incremental)

**Step 1: Add is_locked_by_user to LockManager**
In `backend/app/services/file_service.py` LockManager:

```python
def is_locked_by_user(self, filename: str, user: str) -> bool:  # NEW
    lock_info = self.get_lock_info(filename)
    if not lock_info:
        return False
    return lock_info['user'] == user  # NEW: Ownership check
```

- **Explanation**: Simple equality (CS: predicate). Used for checkin validation.
- **Test**: Lock as "alice", is_locked_by_user("alice", "alice") → True, "bob" → False.
- **Gotcha**: Case-sensitive (normalize usernames).

**Step 2: Update release_lock (Add Ownership)**
Replace release_lock:

```python
def release_lock(self, filename: str, user: str, is_admin: bool = False):  # NEW param
    locks = self.load_locks()
    if filename not in locks:
        raise ValueError("File is not locked")
    if not is_admin and locks[filename]['user'] != user:  # NEW: Check
        raise ValueError(f"Lock owned by {locks[filename]['user']}, not {user}")
    del locks[filename]
    self.save_locks(locks)
    logger.info(f"Lock released: {filename} by {user}")
```

- **Explanation**: is_admin = override (CS: conditional policy). ValueError = explicit (revisit Stage 5).
- **Test**: Release own → OK, other's → ValueError.
- **Gotcha**: Default False = secure (deny by default).

**Step 3: Add force_release (Admin Only)**
Add:

```python
def force_release(self, filename: str):  # NEW
    locks = self.load_locks()
    if filename not in locks:
        raise ValueError("File is not locked")
    del locks[filename]
    self.save_locks(locks)
    logger.warning(f"Lock force-released: {filename}")
```

- **Explanation**: No user param (admin calls directly). Warning = elevated log (SE: alert on sensitive).
- **Test**: Force—unlocks without check.

**Full LockManager** (End of Section—Verify):

```python
class LockManager:
    # ... existing load/save/is_locked/get_lock_info/acquire_lock
    def is_locked_by_user(self, filename: str, user: str) -> bool:
        lock_info = self.get_lock_info(filename)
        if not lock_info:
            return False
        return lock_info['user'] == user
    def release_lock(self, filename: str, user: str, is_admin: bool = False):
        locks = self.load_locks()
        if filename not in locks:
            raise ValueError("File is not locked")
        if not is_admin and locks[filename]['user'] != user:
            raise ValueError(f"Lock owned by {locks[filename]['user']}, not {user}")
        del locks[filename]
        self.save_locks(locks)
        logger.info(f"Lock released: {filename} by {user}")
    def force_release(self, filename: str):
        locks = self.load_locks()
        if filename not in locks:
            raise ValueError("File is not locked")
        del locks[filename]
        self.save_locks(locks)
        logger.warning(f"Lock force-released: {filename}")
```

**Verification**: Checkout as admin, try checkin as john → Error. Force as admin → Unlocks.

### 6.2: Audit Logger (Immutable Trail Incremental)

**Step 1: Add AuditLogger Class**
After LockManager:

```python
class AuditLogger:  # NEW
    def __init__(self, audit_file: Path):
        self.audit_file = audit_file
        if not self.audit_file.exists():
            self.audit_file.write_text('[]')  # NEW: Array
```

- **Explanation**: Array for append (CS: log as stream). Empty start.
- **Test**: Init—creates [].

**Step 2: Add log_action (Append Atomic)**
Add:

```python
    def log_action(self, action: str, filename: str, user: str, details: Optional[dict] = None, success: bool = True):  # NEW
        try:
            with LockedFile(self.audit_file, 'r+') as f:  # Atomic
                content = f.read()
                logs = json.loads(content) if content.strip() else []
                entry = {  # NEW
                    'timestamp': datetime.now(timezone.utc).isoformat(),
                    'action': action,
                    'filename': filename,
                    'user': user,
                    'success': success,
                    'details': details or {}
                }
                logs.append(entry)
                f.seek(0)
                f.truncate()
                json.dump(logs, f, indent=2)
            logger.info(f"AUDIT: {action} {filename} by {user} - {'success' if success else 'failed'}")
        except Exception as e:
            logger.error(f"Audit failed: {e}")
```

- **Explanation**: r+ = read-modify-write atomic (revisit locking). Append = immutable (CS: event sourcing).
- **Test**: Log 'test'—audit.json appends entry.
- **Gotcha**: seek(0)/truncate = reset before write.

**Step 3: Add get_logs (Query)**
Add:

```python
    def get_logs(self, filename: Optional[str] = None, user: Optional[str] = None, limit: int = 100) -> List[dict]:  # NEW
        try:
            with LockedFile(self.audit_file, 'r') as f:
                content = f.read()
                logs = json.loads(content) if content.strip() else []
            results = logs
            if filename:
                results = [log for log in results if log['filename'] == filename]
            if user:
                results = [log for log in results if log['user'] == user]
            return list(reversed(results))[:limit]  # NEW: Recent first
        except Exception as e:
            logger.error(f"Logs read failed: {e}")
            return []
```

- **Explanation**: List comp = filter (CS: functional). Reversed = chronological (app: timeline).
- **Test**: Log 3, get_logs(limit=2) → Last 2.

**Full AuditLogger** (End of Section—Verify):

```python
class AuditLogger:
    def __init__(self, audit_file: Path):
        self.audit_file = audit_file
        if not self.audit_file.exists():
            self.audit_file.write_text('[]')
    def log_action(self, action: str, filename: str, user: str, details: Optional[dict] = None, success: bool = True):
        try:
            with LockedFile(self.audit_file, 'r+') as f:
                content = f.read()
                logs = json.loads(content) if content.strip() else []
                entry = {
                    'timestamp': datetime.now(timezone.utc).isoformat(),
                    'action': action,
                    'filename': filename,
                    'user': user,
                    'success': success,
                    'details': details or {}
                }
                logs.append(entry)
                f.seek(0)
                f.truncate()
                json.dump(logs, f, indent=2)
            logger.info(f"AUDIT: {action} {filename} by {user} - {'success' if success else 'failed'}")
        except Exception as e:
            logger.error(f"Audit failed: {e}")
    def get_logs(self, filename: Optional[str] = None, user: Optional[str] = None, limit: int = 100) -> List[dict]:
        try:
            with LockedFile(self.audit_file, 'r') as f:
                content = f.read()
                logs = json.loads(content) if content.strip() else []
            results = logs
            if filename:
                results = [log for log in results if log['filename'] == filename]
            if user:
                results = [log for log in results if log['user'] == user]
            return list(reversed(results))[:limit]
        except Exception as e:
            logger.error(f"Logs read failed: {e}")
            return []
```

**Verification**: Log 2 actions, get_logs(user="admin") → Filtered list.

### 6.3: Update FileService (Integrate Audit/Ownership Incremental)

**Step 1: Update **init** (Add Audit)**
In FileService **init**:

```python
self.audit_logger = AuditLogger(audit_file)  # NEW: If missing
```

- **Explanation**: Inject audit (SE: dependency).
- **Test**: Init—OK.

**Step 2: Update checkout_file (Audit Happy/Sad)**
In try:

```python
self.audit_logger.log_action('checkout', filename, user, {'message': message})  # NEW success
```

In except:

```python
self.audit_logger.log_action('checkout', filename, user, {'error': str(e)}, success=False)  # NEW fail
```

- **Explanation**: Log both paths (SE: full trail).
- **Test**: Checkout success/fail—audit.json has entries.

**Step 3: Update checkin_file (Ownership + Audit)**
In try:

```python
self.lock_manager.release_lock(filename, user, is_admin)  # Uses new param
self.audit_logger.log_action('checkin', filename, user, {'admin_override': is_admin})
```

In except:

```python
self.audit_logger.log_action('checkin', filename, user, {'error': str(e)}, success=False)
```

- **Explanation**: is_admin passed (revisit release_lock Step 2).
- **Test**: Checkin own/admin → Logs success, other → Error + log.

**Step 4: Add force_checkin (Admin)**
Add:

```python
def force_checkin(self, filename: str, admin_user: str):  # NEW
    lock_info = self.lock_manager.get_lock_info(filename)
    if not lock_info:
        raise ValueError("Not locked")
    original_user = lock_info['user']
    self.lock_manager.force_release(filename)  # NEW
    self.audit_logger.log_action(
        'force_checkin', filename, admin_user,
        {'original_user': original_user, 'reason': 'Admin override'}
    )
```

- **Explanation**: Logs original (audit: who/why).
- **Test**: Force—unlocks, logs.

**Full FileService** (End of Section—Verify):
[Full with audit/ownership in checkout/checkin/force]

**Verification**: Checkout → Audit success. Wrong checkin → Audit fail + ValueError.

### 6.4: Update API for Admin Endpoints (Protected Incremental)

**Step 1: Add force-checkin Endpoint**
In files.py:

```python
@router.post("/admin/force-checkin/{filename}")  # NEW
def force_checkin_file(
    filename: str,
    current_user: User = Depends(require_admin),  # NEW: Admin only
    file_service: FileService = Depends(get_file_service)
):
    try:
        file_service.force_checkin(filename, current_user.username)
        return {"success": True, "message": f"Force-checked {filename}"}
    except ValueError as e:
        raise HTTPException(404, str(e))
    except Exception as e:
        raise HTTPException(500, f"Force failed: {str(e)}")
```

- **Explanation**: require_admin = dep chain (CS: composition). 404 = not locked.
- **Test**: /docs as admin → Success, user → 403.

**Step 2: Add audit-logs Endpoint**
Add:

```python
@router.get("/admin/audit-logs")  # NEW
def get_audit_logs(
    filename: Optional[str] = None,
    user: Optional[str] = None,
    limit: int = 100,
    current_user: User = Depends(require_admin),
    file_service: FileService = Depends(get_file_service)
):
    try:
        logs = file_service.get_audit_logs(filename, user, limit)  # Assume added
        return {"logs": logs, "count": len(logs)}
    except Exception as e:
        raise HTTPException(500, f"Logs failed: {str(e)}")
```

- **Add to FileService**:
  ```python
  def get_audit_logs(self, filename: Optional[str] = None, user: Optional[str] = None, limit: int = 100) -> List[dict]:
      return self.audit_logger.get_logs(filename, user, limit=limit)
  ```
- **Explanation**: Query params = filter (CS: SQL-like). Limit = paginate.
- **Test**: /api/files/admin/audit-logs?user=admin → Logs JSON.

**Full files.py** (End of Section—Verify):
[Full with protected get_files, checkout/checkin using token user, admin endpoints]

**Verification**: /api/files requires token. Force as admin → Works.

### 6.5: Frontend - Admin Dashboard & Audit Modal (Tailwind Incremental)

**Step 1: Add Admin Panel to index.html**
After <header>:

```html
<div id="admin-panel-container"></div>
# NEW
```

- **Explanation**: Container for conditional (JS renders if admin).
- **Test**: Empty div present.

**Step 2: Add Audit Modal**
Before </body>:

```html
<div id="audit-modal" class="modal-overlay hidden">
  # NEW
  <div class="modal-content max-w-4xl">
    # Tailwind wide
    <div class="modal-header">
      <h3>Audit Logs</h3>
      <button class="modal-close">&times;</button>
    </div>
    <div class="modal-body">
      <div class="flex gap-3 mb-4">
        # Filters
        <input
          type="text"
          id="audit-filename-filter"
          placeholder="Filter by filename"
          class="flex-1 p-3 border rounded"
        />
        <input
          type="text"
          id="audit-user-filter"
          placeholder="Filter by user"
          class="flex-1 p-3 border rounded"
        />
        <button class="btn btn-primary px-4 py-2" id="audit-search-btn">
          Search
        </button>
      </div>
      <div id="audit-logs-container" class="max-h-96 overflow-y-auto"></div>
      # Scroll
    </div>
  </div>
</div>
```

- **Explanation**: Flex gap = row (Tailwind). max-h-96 = scroll height.
- **Test**: Add .open—modal with filters.

**Step 3: Add Admin Styles (Tailwind Layer)**
In input.css @layer components:

```css
@layer components {
  # NEW .admin-panel {
    @apply bg-warning/10 border-2 border-warning rounded-lg p-6 mb-6;
  }
  # NEW .admin-panel h3 {
    @apply text-warning mb-4 flex items-center gap-2;
  }
  # NEW .admin-actions {
    @apply flex gap-3 flex-wrap mt-4;
  }
  # NEW .audit-log-entry {
    @apply p-4 border border-default rounded-md mb-3 bg-secondary;
  }
  # NEW .audit-log-entry.failed {
    @apply border-l-4 border-danger;
  }
  .audit-log-entry.success {
    @apply border-l-4 border-success;
  }
  .audit-log-header {
    @apply flex justify-between items-center mb-2;
  }
  .audit-log-action {
    @apply font-semibold text-primary;
  }
  .audit-log-time {
    @apply text-sm text-secondary;
  }
  .audit-log-details {
    @apply text-sm text-secondary;
  }
}
```

Rebuild tailwind.css.

- **Explanation**: @layer = order (after base). /10 = opacity (Tailwind arbitrary).
- **Test**: <div class="admin-panel"> → Warning bg.

**Step 4: Wire Admin Panel in app.js**
In DOMContentLoaded:

```javascript
const userRole = localStorage.getItem("user_role");  # NEW
renderAdminPanel(userRole);  # NEW
```

Add:

```javascript
function renderAdminPanel(role) {  # NEW
  const container = document.getElementById("admin-panel-container");
  if (role !== "admin") {  # NEW
    container.innerHTML = "";
    return;
  }
  container.innerHTML = `
    <div class="container pt-6">
      <div class="admin-panel">
        <h3>⚠️ Admin Panel</h3>
        <p class="mb-4 text-secondary">Administrative privileges. Use responsibly.</p>
        <div class="admin-actions">
          <button class="btn btn-secondary btn-sm" id="view-audit-logs-btn">📋 View Audit Logs</button>
        </div>
      </div>
    </div>
  `;
  document.getElementById("view-audit-logs-btn").addEventListener("click", showAuditLogs);  # NEW
}
```

- **Explanation**: Conditional render (JS: if). Tailwind = pretty panel.
- **Test**: Login admin—panel shows, button.
- **Gotcha**: localStorage from Stage 5.

**Step 5: Add showAuditLogs (Fetch/Modal)**
Add:

```javascript
const auditModal = new ModalManager("audit-modal");  # NEW instance

async function showAuditLogs() {  # NEW
  auditModal.open();
  loadAuditLogs();
}
async function loadAuditLogs(filename = null, user = null) {  # NEW
  const container = document.getElementById("audit-logs-container");
  container.innerHTML = '<div class="loading">Loading...</div>';  # Tailwind
  try {
    const params = { limit: 50 };
    if (filename) params.filename = filename;
    if (user) params.user = user;
    const data = await apiClient.getAuditLogs(params);  # NEW call
    if (data.logs.length === 0) {
      container.innerHTML = '<div class="text-center py-8 text-secondary">No logs.</div>';
      return;
    }
    container.innerHTML = data.logs.map((log) => {  # NEW
      const date = new Date(log.timestamp);
      const statusClass = log.success ? "success" : "failed";
      return `
        <div class="audit-log-entry ${statusClass}">
          <div class="audit-log-header">
            <div class="audit-log-action">${log.action.toUpperCase()}: ${log.filename}</div>
            <div class="audit-log-time">${date.toLocaleString()}</div>
          </div>
          <div class="audit-log-details">
            <strong>User:</strong> ${log.user} <strong>Status:</strong> ${log.success ? "✓" : "✗"}
            ${log.details ? `<br><strong>Details:</strong> ${JSON.stringify(log.details)}` : ''}
          </div>
        </div>
      `;
    }).join("");
  } catch (error) {
    container.innerHTML = `<div class="text-center py-8 text-danger">Error: ${error.message}</div>`;
  }
}
```

- **Add to api-client.js**:
  ```javascript
  async getAuditLogs(params = {}) {  # NEW
    const query = new URLSearchParams(params).toString();
    return this.get(`/api/files/admin/audit-logs${query ? '?' + query : ''}`);
  }
  ```
- **Explanation**: URLSearchParams = query string (JS: encode). Map/join = render (CS: transformation).
- **Test**: Click button—modal, fetches/logs.
- **Gotcha**: JSON.stringify = safe display.

**Step 6: Wire Filter Button**
In DOMContentLoaded:

```javascript
document.getElementById("audit-search-btn").addEventListener("click", () => {  # NEW
  const filename = document.getElementById("audit-filename-filter").value;
  const user = document.getElementById("audit-user-filter").value;
  loadAuditLogs(filename || null, user || null);
});
```

- **Explanation**: Value = input (event value). || null = optional.
- **Test**: Type filter, search—reloads filtered.

**Full app.js** (End of Section—Verify):
[Full with admin render, audit functions, Tailwind classes in HTML]

**Verification**: Login admin—panel + logs modal. Filter works, pretty with Tailwind.

### Stage 6 Complete

**Test Full**: Checkout as john, audit logs show. Admin force—unlocks.

**Verification**:

- [ ] Ownership blocks wrong checkin.
- [ ] Audit logs all actions.
- [ ] Admin panel/logs only for admin.
- [ ] Tailwind = clean UI.

**What You Learned (Depth)**:

- **CS**: RBAC (matrices), append-only logs (immutability).
- **App**: Force ops (recovery), filters (queries).
- **Python**: Decorator factories (higher-order).
- **JS**: Map/join (functional render).
- **SE**: Audit trail (compliance), conditional UI (roles).

Ready for Stage 7 (Git)?
