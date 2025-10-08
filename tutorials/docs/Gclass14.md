# Step 14: Full Forms & Uploads – Handling File Inputs (Multipart Magic – 1.5hr)

**Big Picture Goal**: Expand checkin modal to upload files (FormData multipart), backend receives/saves + commits to Git. Understand **multipart forms** (text + binary like files) and **upload flow** (client send → server write → persist).

**Why Fourteenth?** (Form Principle: **Inputs After Actions – Complete the Loop**). Checkout/checkin buttons work; now full checkin = upload form (file + message). **Deep Dive**: Multipart = "mixed payload" (text fields + binary files)—essential for uploads. Why Git commit? Version files (CNC edits = traceable). Resource: [MDN FormData Multipart](https://developer.mozilla.org/en-US/docs/Web/API/FormData/Using_FormData_Objects) – 4min, "Sending files."

**When**: After modals—forms need dynamic UI. Use for uploads (e.g., G-code file submit).

**How**: JS FormData.append(file), fetch POST. Backend: UploadFile = read bytes, write to repo. Gotcha: Large files = timeout (chunk later).

**Pre-Step**: Branch: `git checkout -b step-14-uploads`. Update checkin template in modalManager: Add `<input type="file" id="checkinFile" /> <textarea id="commitMessage"></textarea> <button data-action="submitCheckin">Submit</button>`. Backend mock /files/test.mcam/checkin: `@router.post("/files/{filename}/checkin") async def checkin(filename: str, file: UploadFile = File(...)): return {"status": "uploaded"}`.

---

### 14a: Client Form with File Input – Multipart Prep

**Question**: How do we add file upload to checkin form? We need input type="file" + FormData for mixed data (message + file).

**Micro-Topic 1: File Input in Template**  
**Type This (update buildCheckinModal in ui/modalManager.js)**:

```javascript
function buildCheckinModal(filename) {
  return `<div class="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
    <div class="bg-white p-6 rounded shadow-lg">
      <h3>Check In: ${filename}</h3>
      <textarea id="commitMessage" placeholder="Changes..." class="block w-full mb-2 p-2 border rounded"></textarea>
      <input type="file" id="checkinFile" accept=".mcam" class="block w-full mb-2 p-2 border rounded" />  // What: File picker.
      <button data-action="submitCheckin" class="bg-blue-500 text-white px-4 py-2 rounded">Submit</button>
    </div>
  </div>`;
}
```

**Inline 3D Explain**:

- **What**: type="file" = browser picker. accept = filter (.mcam only).
- **Why**: File = binary input (text = easy, files = multipart). **Deep Dive**: accept = UX hint (no .txt). Resource: [MDN File Input](https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input/file) – 2min, "Accept."
- **How**: id = JS target. Gotcha: No multiple = one file. **Alternative**: Drag-drop = fancy, but file = standard.

**Try This (10s)**: Open checkin modal → file input? Click → picker, select .mcam? Tweak: Remove accept → all files. Reflect: "Why id? Target for FormData.append(document.getElementById('checkinFile').files[0])."

**Inline Lens (SRP Integration)**: Template = UI only (no submit logic—delegation). Violate? Add fetch here = mixed.

**Mini-Summary**: type="file" = binary input. accept = filter UX.

**Micro-Topic 2: FormData for Mixed Data**  
**Type This (add to ui/fileManager.js checkinFile stub)**:

```javascript
export async function checkinFile(filename) {
  const message = document.getElementById("commitMessage").value; // Text field.
  const fileInput = document.getElementById("checkinFile"); // File picker.
  const file = fileInput.files[0]; // First file.

  const formData = new FormData(); // What: Multipart builder.
  formData.append("message", message); // Text.
  formData.append("file", file); // Binary.

  console.log("Form ready:", message, file.name); // Test.
}
```

**Inline 3D Explain**:

- **What**: files[0] = selected file obj. append = add to body.
- **Why**: FormData = mixed (text + file in one POST). **Deep Dive**: Auto Content-Type = multipart/form-data (boundary separates). Resource: [MDN FormData Append](https://developer.mozilla.org/en-US/docs/Web/API/FormData/append) – 2min, "File."
- **How**: fileInput.files = array. Gotcha: No [0] = null file error. **Alternative**: JSON + base64 file = huge (multipart = efficient).

**Try This (15s)**: Open checkin → fill message, select file → console "Form ready: Changes... test.mcam"? Tweak: No file → undefined. Reflect: "Why FormData? JSON = no binary—files corrupt."

**Inline Lens (Error Handling Integration)**: Guard file [0] next (if !file = error). Violate? Null append = bad POST.

**Mini-Summary**: FormData.append = mixed payload. files[0] = selected.

**Git**: `git add modalManager.js fileManager.js && git commit -m "feat(step-14a): checkin form + FormData"`.

---

### 14b: Client Upload Flow – Submit to Backend

**Question**: How do we send FormData to /files/{filename}/checkin? We need fetch POST + success notify + re-render.

**Micro-Topic 1: Fetch POST with FormData**  
**Type This (update checkinFile)**:

```javascript
export async function checkinFile(filename) {
  // ... from 14a (message, file).
  if (!file) return showNotification("Select file", "error"); // Guard.

  try {
    const response = await fetch(`/files/${filename}/checkin`, {
      // URL with param.
      method: "POST",
      body: formData, // Multipart auto.
    });
    if (!response.ok) throw new Error("Upload failed");
    showNotification("Checked in!"); // Success.
    await loadFiles(); // Re-fresh UI.
  } catch (error) {
    showNotification(error.message, "error");
  }
}
```

**Inline 3D Explain**:

- **What**: body: formData = send mixed. /${filename} = dynamic URL.
- **Why**: POST = mutate (upload = change). **Deep Dive**: No Content-Type = auto (from FormData). Resource: [MDN Fetch Body](https://developer.mozilla.org/en-US/docs/Web/API/Fetch_API/Using_Fetch#supplying_request_options) – 2min, "Body."
- **How**: Guard = early fail. Gotcha: Large file = timeout (add signal later). **Alternative**: PUT = update known—POST = create new rev.

**Try This (20s)**: Open checkin → fill/select → submit → "Checked in!" + re-render? Backend mock 200 → success? Fail mock → error. Tweak: No guard → submits null file (backend crash). Reflect: "Why re-loadFiles? Local status update = stale for others."

**Inline Lens (Error Handling Integration)**: Guard + try = layered (client = fast, catch = all). Violate? No guard = bad data to server.

**Mini-Summary**: Fetch POST body = upload send. Guard = input safe.

**Micro-Topic 2: Wire Submit in Delegation**  
**Type This (update main.js delegation)**:

```javascript
case "submitCheckin":
  const filename = modal.dataset.filename || 'default';  // From open data.
  await checkinFile(filename);  // Call.
  break;
```

**Inline 3D Explain**:

- **What**: modal.dataset.filename = pass from open (modal.id or data).
- **Why**: Wire = "intent to action." **Deep Dive**: Delegation = scoped (modal listener catches). Resource: [MDN Delegation](https://developer.mozilla.org/en-US/docs/Learn/JavaScript/Building_blocks/Events#event_delegation) – 2min.
- **How**: dataset = camel. Gotcha: No data = default. **Alternative**: Global var = coupling bad.

**Try This (15s)**: Open checkin with data-filename="test" (in open call) → submit → calls with "test"? Tweak: Wrong = default. Reflect: "Why dataset? Pass context without globals."

**Inline Lens (Coupling Integration)**: Delegation = loose (button = intent, main = route). Violate? Hardcode filename = wrong file.

**Mini-Summary**: Delegation wire = submit to call. Dataset = param pass.

**Git**: `git add main.js fileManager.js && git commit -m "feat(step-14b): upload flow + wire"`.

---

### 14c: Backend Upload Handling – Receive & Save File

**Question**: How does backend receive file + message? We need UploadFile = read bytes, write to repo + commit.

**Micro-Topic 1: Route with UploadFile**  
**Type This (update backend/endpoints.py checkin)**:

```python
from fastapi import UploadFile, File, Form

@router.post("/files/{filename}/checkin")
async def checkin_file(
  filename: str,
  message: str = Form(...),  // Text field.
  file: UploadFile = File(...)  // Binary file.
):
  content = await file.read()  // What: Bytes from upload.
  print(f"Received {len(content)} bytes for {filename}");  // Test.
  return {"status": "uploaded"}
```

**Inline 3D Explain**:

- **What**: File(...) = extract binary. read() = async bytes.
- **Why**: UploadFile = multipart parse. **Deep Dive**: await read = stream (large = no mem flood). Resource: [FastAPI Upload](https://fastapi.tiangolo.com/tutorial/request-files/) – 3min, "UploadFile."
- **How**: Form = text. Gotcha: No await = empty. **Alternative**: Bytes body = no metadata (name/type).

**Try This (10s)**: Postman POST /files/test.mcam/checkin (Body form-data: message="test", file=select .mcam) → "Received X bytes"? Tweak: No file → error? Reflect: "Why read? File = stream—read = full bytes."

**Micro-Topic 2: Save File to Repo**  
**Type This (add to checkin_file)**:

```python
from pathlib import Path

repo_path = Path(".") / filename  // What: Path = file location.
repo_path.parent.mkdir(exist_ok=True);  // Dir if needed.
repo_path.write_bytes(content)  // Write bytes.
print(f"Saved {filename}");  // Test.
```

**Inline 3D Explain**:

- **What**: Path = file handle. write_bytes = dump binary.
- **Why**: Save = persist (upload = file on disk). **Deep Dive**: mkdir parents = auto-dirs. Resource: [Pathlib Write](https://docs.python.org/3/library/pathlib.html#pathlib.Path.write_bytes) – 2min.
- **How**: . = current dir. Gotcha: No parent = error (mkdir fixes). **Alternative**: open/write = manual close (with = auto).

**Try This (15s)**: POST → test.mcam created? Size matches? Tweak: Bad dir → mkdir fixes. Reflect: "Why bytes? Text = decode error on binary."

**Micro-Topic 3: Commit Save to Git**  
**Type This (add, import git)**:

```python
import git

repo = git.Repo(".")  // Open repo.
repo.git.add(str(repo_path))  // Stage.
repo.index.commit(f"Checkin {filename}: {message}")  // Message from form.
print("Committed");  // Test.
```

**Inline 3D Explain**:

- **What**: add = stage, commit = snapshot.
- **Why**: Commit = version (audit "who/when changed"). **Deep Dive**: index = staging (add prep). Resource: [GitPython Commit](https://gitpython.readthedocs.io/en/stable/reference.html#git.index.BaseIndexEntry.commit) – 2min.
- **How**: f-string = format. Gotcha: No push = local (add repo.git.push()). **Alternative**: No Git = file only (lost on delete).

**Try This (20s)**: POST → git log → "Checkin test.mcam: test"? Tweak: No message = default. Reflect: "Why commit? File = ephemeral—Git = history."

**Inline Lens (SRP Integration)**: endpoints = route, git_repo.py = commit (import later). Violate? Commit here = mixed.

**Mini-Summary**: UploadFile + write + commit = full upload.

**Git**: `git add endpoints.py && git commit -m "feat(step-14c): backend upload + commit"`.

---

**Step 14 Complete!** Uploads full. Reflect: "Flow: Open form → fill/file → FormData POST → backend read/write/commit → success + re-render. SRP: FormData = prep, backend = persist."

**Next**: Step 15: Admin Extras (repo switch, LFS, users). Go? 🚀
