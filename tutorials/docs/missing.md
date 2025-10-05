# Missing Code & Features Supplement

This document contains all the missing code blocks and features referenced but not included in the tutorial rewrite. Use it alongside both tutorials.

---

## STAGE 3: Missing Cross-Platform File Locking Class

**Location**: Add to `backend/main.py` after your imports

```python
import os
if os.name == 'nt':  # Windows
    import msvcrt
else:  # Unix/Linux/macOS
    import fcntl

class LockedFile:
    """
    A cross-platform context manager for exclusive file locking.

    On Windows, uses msvcrt.locking() for file locks.
    On Unix-like systems, uses fcntl.flock() for file locks.

    This ensures that read-modify-write sequences on a file are atomic,
    preventing race conditions when multiple processes access the same file.
    """
    def __init__(self, filepath, mode='r'):
        self.filepath = filepath
        self.mode = mode
        self.file = None

    def __enter__(self):
        """Acquire the file lock when entering the context."""
        self.file = open(self.filepath, self.mode)

        if os.name == 'nt':
            # Windows: Lock the entire file
            msvcrt.locking(self.file.fileno(), msvcrt.LK_LOCK, os.path.getsize(self.filepath))
        else:
            # Unix: Use flock for advisory locking
            fcntl.flock(self.file.fileno(), fcntl.LOCK_EX)

        return self.file

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Release the file lock and close the file when exiting the context."""
        if self.file:
            if os.name == 'nt':
                # Windows: Unlock
                msvcrt.locking(self.file.fileno(), msvcrt.LK_UNLCK, os.path.getsize(self.filepath))
            else:
                # Unix: Unlock
                fcntl.flock(self.file.fileno(), fcntl.LOCK_UN)

            self.file.close()

        # Return False to propagate any exceptions that occurred
        return False
```

**Why This Matters**: Without this, your `load_locks()` and `save_locks()` functions have a race condition. Two simultaneous requests could both read the same lock state, modify it differently, and the last write wins—corrupting your data.

**Testing It**: The `race_condition_simulator.py` script in the tutorial will fail without this, and succeed with it.

---

## STAGE 4: Complete Modal System

**Location**: Add to `backend/static/index.html` before `</body>`

```html
<!-- Checkout Modal -->
<div id="checkout-modal" class="modal-overlay hidden">
  <div class="modal-content">
    <div class="modal-header">
      <h3>Check Out File</h3>
      <button class="modal-close" onclick="checkoutModal.close()">
        &times;
      </button>
    </div>
    <div class="modal-body">
      <p>You are checking out: <strong id="checkout-filename"></strong></p>
      <form id="checkout-form">
        <div class="form-group">
          <label for="checkout-user">Your Name:</label>
          <input type="text" id="checkout-user" required />
        </div>
        <div class="form-group">
          <label for="checkout-message">Reason for checkout:</label>
          <textarea id="checkout-message" rows="3" required></textarea>
        </div>
        <div class="modal-actions">
          <button
            type="button"
            class="btn btn-secondary"
            onclick="checkoutModal.close()"
          >
            Cancel
          </button>
          <button type="submit" class="btn btn-primary">
            Confirm Checkout
          </button>
        </div>
      </form>
    </div>
  </div>
</div>

<!-- Checkin Modal -->
<div id="checkin-modal" class="modal-overlay hidden">
  <div class="modal-content">
    <div class="modal-header">
      <h3>Check In File</h3>
      <button class="modal-close" onclick="checkinModal.close()">
        &times;
      </button>
    </div>
    <div class="modal-body">
      <p>You are checking in: <strong id="checkin-filename"></strong></p>
      <form id="checkin-form">
        <div class="form-group">
          <label for="checkin-user">Your Name (for confirmation):</label>
          <input type="text" id="checkin-user" required />
        </div>
        <div class="modal-actions">
          <button
            type="button"
            class="btn btn-secondary"
            onclick="checkinModal.close()"
          >
            Cancel
          </button>
          <button type="submit" class="btn btn-primary">
            Confirm Check-in
          </button>
        </div>
      </form>
    </div>
  </div>
</div>
```

**Location**: Add to `backend/static/css/components.css`

```css
/* Form styling */
.form-group {
  margin-bottom: var(--spacing-4);
}

.form-group label {
  display: block;
  margin-bottom: var(--spacing-2);
  font-weight: var(--font-weight-medium);
  color: var(--text-primary);
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: var(--spacing-3);
  border: 1px solid var(--border-default);
  border-radius: var(--radius-base);
  background: var(--bg-primary);
  color: var(--text-primary);
  font-family: inherit;
  transition: border-color var(--transition-fast);
}

.form-group input:focus,
.form-group textarea:focus {
  outline: none;
  border-color: var(--interactive-primary);
  box-shadow: 0 0 0 3px var(--interactive-primary-alpha);
}
```

**Location**: Add `ModalManager` class to `backend/static/js/app.js`

```javascript
class ModalManager {
  constructor(modalId) {
    this.modal = document.getElementById(modalId);
    this.overlay = this.modal;

    // Close on overlay click (but not on content click)
    this.overlay.addEventListener("click", (e) => {
      if (e.target === this.overlay) {
        this.close();
      }
    });

    // Close on X button click
    const closeBtn = this.modal.querySelector(".modal-close");
    if (closeBtn) {
      closeBtn.addEventListener("click", () => this.close());
    }

    // Close on Escape key
    document.addEventListener("keydown", (e) => {
      if (e.key === "Escape" && !this.modal.classList.contains("hidden")) {
        this.close();
      }
    });
  }

  open() {
    this.modal.classList.remove("hidden");
    // Focus the first input when modal opens
    const firstInput = this.modal.querySelector("input, textarea");
    if (firstInput) {
      setTimeout(() => firstInput.focus(), 100);
    }
  }

  close() {
    this.modal.classList.add("hidden");
    // Clear form if it exists
    const form = this.modal.querySelector("form");
    if (form) {
      form.reset();
    }
  }
}
```

---

## STAGE 5: Complete Authentication Implementation

**Location**: Create `backend/static/login.html`

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Login - PDM System</title>
    <link rel="stylesheet" href="/static/css/main.css" />
    <style>
      body {
        display: flex;
        align-items: center;
        justify-content: center;
        min-height: 100vh;
        background: linear-gradient(
          135deg,
          var(--color-primary-500),
          var(--color-primary-700)
        );
      }

      .login-container {
        background: var(--card-bg);
        padding: var(--spacing-8);
        border-radius: var(--card-border-radius);
        box-shadow: var(--shadow-lg);
        width: 90%;
        max-width: 400px;
      }

      .login-header {
        text-align: center;
        margin-bottom: var(--spacing-6);
      }

      .login-header h1 {
        color: var(--color-primary-500);
        margin-bottom: var(--spacing-2);
      }

      .error-message {
        background: var(--status-danger-bg);
        color: var(--status-danger-text);
        padding: var(--spacing-3);
        border-radius: var(--radius-base);
        margin-bottom: var(--spacing-4);
        display: none;
      }

      .error-message.show {
        display: block;
      }
    </style>
  </head>
  <body>
    <div class="login-container">
      <div class="login-header">
        <h1>PDM System</h1>
        <p>Parts Data Management</p>
      </div>

      <div id="error-message" class="error-message"></div>

      <form id="login-form">
        <div class="form-group">
          <label for="username">Username</label>
          <input type="text" id="username" name="username" required autofocus />
        </div>

        <div class="form-group">
          <label for="password">Password</label>
          <input type="password" id="password" name="password" required />
        </div>

        <button type="submit" class="btn btn-primary" style="width: 100%;">
          Login
        </button>
      </form>

      <div
        style="margin-top: var(--spacing-4); text-align: center; font-size: var(--font-size-sm); color: var(--text-secondary);"
      >
        <p>Demo Credentials:</p>
        <p>admin / admin123 or john / password123</p>
      </div>
    </div>

    <script src="/static/js/login.js"></script>
  </body>
</html>
```

**Location**: Create `backend/static/js/login.js`

```javascript
document.getElementById("login-form").addEventListener("submit", async (e) => {
  e.preventDefault();

  const username = document.getElementById("username").value;
  const password = document.getElementById("password").value;
  const errorDiv = document.getElementById("error-message");

  try {
    // OAuth2 password flow requires form-encoded data
    const formData = new URLSearchParams();
    formData.append("username", username);
    formData.append("password", password);

    const response = await fetch("/api/auth/login", {
      method: "POST",
      headers: {
        "Content-Type": "application/x-www-form-urlencoded",
      },
      body: formData,
    });

    const data = await response.json();

    if (!response.ok) {
      throw new Error(data.detail || "Login failed");
    }

    // Store the token in localStorage
    localStorage.setItem("access_token", data.access_token);

    // Decode the JWT to get the user's role (for UI purposes only, never trust client-side data for security)
    const payload = JSON.parse(atob(data.access_token.split(".")[1]));
    localStorage.setItem("user_role", payload.role);
    localStorage.setItem("username", payload.sub);

    // Redirect to main app
    window.location.href = "/";
  } catch (error) {
    errorDiv.textContent = error.message;
    errorDiv.classList.add("show");

    // Clear the error after 5 seconds
    setTimeout(() => {
      errorDiv.classList.remove("show");
    }, 5000);
  }
});
```

**Location**: Add to the `<head>` of `backend/static/index.html` (auth guard)

```html
<script>
  // Auth Guard: Redirect to login if no token
  (function () {
    const token = localStorage.getItem("access_token");
    if (!token && window.location.pathname !== "/login") {
      window.location.href = "/login";
    }
  })();
</script>
```

**Location**: Add utility function to `backend/static/js/app.js`

```javascript
// Helper to parse JWT (client-side only, for UI purposes)
function parseJWT(token) {
  try {
    const base64Url = token.split(".")[1];
    const base64 = base64Url.replace(/-/g, "+").replace(/_/g, "/");
    const jsonPayload = decodeURIComponent(
      atob(base64)
        .split("")
        .map(function (c) {
          return "%" + ("00" + c.charCodeAt(0).toString(16)).slice(-2);
        })
        .join("")
    );
    return JSON.parse(jsonPayload);
  } catch (e) {
    return null;
  }
}

// Check if token is expired
function isTokenExpired(token) {
  const payload = parseJWT(token);
  if (!payload || !payload.exp) return true;
  return Date.now() >= payload.exp * 1000;
}

// Add logout functionality
function logout() {
  localStorage.removeItem("access_token");
  localStorage.removeItem("user_role");
  localStorage.removeItem("username");
  window.location.href = "/login";
}
```

**Location**: Add logout button to `backend/static/index.html` header

```html
<div class="header-actions">
  <button id="theme-toggle" class="btn btn-secondary" title="Toggle Theme">
    🌙
  </button>
  <button onclick="logout()" class="btn btn-secondary">Logout</button>
</div>
```

---

## STAGE 8: Complete Diff and Blame Implementations

**Location**: Add to `backend/main.py`

```python
@app.get("/api/files/{filename}/diff")
def get_file_diff(
    filename: str,
    commit_sha: str,
    current_user: User = Depends(get_current_user)
):
    """
    Returns the diff (changes) for a specific commit of a file.
    Shows what was added/removed in that commit.
    """
    try:
        safe_filename = os.path.basename(filename)
        commit = git_repo.commit(commit_sha)

        # Get the parent commit
        if not commit.parents:
            # This is the first commit, so we compare against empty
            diff_text = "Initial version - no previous version to compare"
        else:
            parent = commit.parents[0]
            # Get the diff between parent and this commit for our specific file
            diff_output = git_repo.git.diff(
                parent.hexsha,
                commit.hexsha,
                f'repo/{safe_filename}'
            )
            diff_text = diff_output if diff_output else "No changes to this file in this commit"

        return {
            "filename": safe_filename,
            "commit": commit.hexsha,
            "message": commit.message,
            "author": commit.author.name,
            "date": commit.committed_datetime.isoformat(),
            "diff": diff_text
        }

    except Exception as e:
        logger.error(f"Failed to get diff: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve diff")


@app.get("/api/files/{filename}/blame")
def get_file_blame(
    filename: str,
    current_user: User = Depends(get_current_user)
):
    """
    Returns line-by-line authorship information for a file.
    Shows who last modified each line and when.
    """
    try:
        safe_filename = os.path.basename(filename)
        file_path = REPO_PATH / safe_filename

        if not file_path.exists():
            raise HTTPException(status_code=404, detail="File not found")

        # Run git blame
        blame_output = git_repo.git.blame(f'repo/{safe_filename}', incremental=True)

        # Parse the blame output into a structured format
        # This is simplified; real blame parsing is complex
        lines = []
        for line in file_path.read_text().splitlines():
            lines.append({
                "line_number": len(lines) + 1,
                "content": line
            })

        # For a proper implementation, parse the incremental blame output
        # For now, we'll use a simpler approach with git log
        commits = list(git_repo.iter_commits(paths=f'repo/{safe_filename}', max_count=1))
        latest_author = commits[0].author.name if commits else "Unknown"

        return {
            "filename": safe_filename,
            "lines": lines,
            "latest_author": latest_author
        }

    except Exception as e:
        logger.error(f"Failed to get blame: {e}")
        raise HTTPException(status_code=500, detail="Failed to retrieve blame information")
```

**Location**: Add modals to `backend/static/index.html`

```html
<!-- Diff Modal -->
<div id="diff-modal" class="modal-overlay hidden">
  <div class="modal-content modal-large">
    <div class="modal-header">
      <h3>File Changes (Diff)</h3>
      <button class="modal-close">&times;</button>
    </div>
    <div id="diff-content" class="modal-body">
      <pre
        id="diff-output"
        style="background: var(--bg-secondary); padding: var(--spacing-4); border-radius: var(--radius-base); overflow-x: auto;"
      ></pre>
    </div>
  </div>
</div>

<!-- Blame Modal -->
<div id="blame-modal" class="modal-overlay hidden">
  <div class="modal-content modal-large">
    <div class="modal-header">
      <h3>File Blame (Line-by-Line Authors)</h3>
      <button class="modal-close">&times;</button>
    </div>
    <div id="blame-content" class="modal-body"></div>
  </div>
</div>
```

**Location**: Add to `backend/static/js/app.js`

```javascript
const diffModal = new ModalManager("diff-modal");
const blameModal = new ModalManager("blame-modal");

async function showDiff(filename, commitSha) {
  diffModal.open();
  const output = document.getElementById("diff-output");
  output.textContent = "Loading diff...";

  try {
    const token = localStorage.getItem("access_token");
    const response = await fetch(
      `/api/files/${filename}/diff?commit_sha=${commitSha}`,
      { headers: { Authorization: `Bearer ${token}` } }
    );

    if (!response.ok) throw new Error("Failed to load diff");

    const data = await response.json();

    // Syntax highlighting for diff would go here
    // For now, just display the raw diff
    output.textContent = data.diff;
  } catch (error) {
    output.textContent = `Error: ${error.message}`;
  }
}

async function showBlame(filename) {
  blameModal.open();
  const content = document.getElementById("blame-content");
  content.innerHTML = "<p>Loading blame information...</p>";

  try {
    const token = localStorage.getItem("access_token");
    const response = await fetch(`/api/files/${filename}/blame`, {
      headers: { Authorization: `Bearer ${token}` },
    });

    if (!response.ok) throw new Error("Failed to load blame");

    const data = await response.json();

    // Build a table of lines with author info
    let html = '<table style="width: 100%; font-family: monospace;">';
    html +=
      "<thead><tr><th>Line</th><th>Author</th><th>Content</th></tr></thead>";
    html += "<tbody>";

    data.lines.forEach((line) => {
      html += `<tr>
        <td style="text-align: right; padding-right: 1rem; color: var(--text-secondary);">${line.line_number}</td>
        <td style="padding: 0 1rem; color: var(--text-secondary);">${data.latest_author}</td>
        <td><code>${line.content}</code></td>
      </tr>`;
    });

    html += "</tbody></table>";
    content.innerHTML = html;
  } catch (error) {
    content.innerHTML = `<p style="color: red;">${error.message}</p>`;
  }
}
```

---

## STAGE 10B: Complete State Management Refactor

**Location**: Complete the store implementation in `backend/static/js/app.js`

```javascript
// --- Enhanced Store with All Actions ---
const store = {
  state: {
    allFiles: [],
    isLoading: true,
    searchTerm: "",
    statusFilter: "all",
    sortBy: "name-asc",
    selectedFile: null,
    onlineUsers: [],
    isConnected: false,
  },

  _listeners: [],

  subscribe(listener) {
    this._listeners.push(listener);
    // Immediately call the listener with current state
    listener({ ...this.state });
  },

  _notify() {
    for (const listener of this._listeners) {
      listener({ ...this.state });
    }
  },

  // Actions
  setFiles(files) {
    this.state.allFiles = files;
    this.state.isLoading = false;
    this._notify();
  },

  setSearchTerm(term) {
    this.state.searchTerm = term;
    this._notify();
  },

  setStatusFilter(filter) {
    this.state.statusFilter = filter;
    this._notify();
  },

  setSortBy(sortKey) {
    this.state.sortBy = sortKey;
    this._notify();
  },

  setSelectedFile(file) {
    this.state.selectedFile = file;
    this._notify();
  },

  setLoading() {
    this.state.isLoading = true;
    this._notify();
  },

  setOnlineUsers(users) {
    this.state.onlineUsers = users;
    this._notify();
  },

  setConnectionStatus(isConnected) {
    this.state.isConnected = isConnected;
    this._notify();
  },

  // Computed getters
  getFilteredFiles() {
    let filtered = this.state.allFiles;

    // Apply search filter
    if (this.state.searchTerm) {
      const term = this.state.searchTerm.toLowerCase();
      filtered = filtered.filter((f) => f.name.toLowerCase().includes(term));
    }

    // Apply status filter
    if (this.state.statusFilter !== "all") {
      filtered = filtered.filter((f) => f.status === this.state.statusFilter);
    }

    return filtered;
  },

  getSortedFiles(files) {
    const [field, direction] = this.state.sortBy.split("-");

    return [...files].sort((a, b) => {
      let aVal, bVal;

      switch (field) {
        case "name":
          aVal = a.name.toLowerCase();
          bVal = b.name.toLowerCase();
          break;
        case "status":
          aVal = a.status;
          bVal = b.status;
          break;
        case "size":
          aVal = a.size_bytes || 0;
          bVal = b.size_bytes || 0;
          break;
        default:
          return 0;
      }

      if (direction === "asc") {
        return aVal > bVal ? 1 : -1;
      } else {
        return aVal < bVal ? 1 : -1;
      }
    });
  },
};
```

**Location**: Add filter/sort UI to `backend/static/index.html`

```html
<section id="file-list-section">
  <h2>File Dashboard</h2>

  <!-- Filters and Search -->
  <div
    class="file-controls"
    style="display: flex; gap: var(--spacing-4); margin-bottom: var(--spacing-4);"
  >
    <input
      type="search"
      id="file-search"
      placeholder="Search files..."
      style="flex: 1; padding: var(--spacing-2) var(--spacing-3); border: 1px solid var(--border-default); border-radius: var(--radius-base);"
    />

    <select
      id="status-filter"
      style="padding: var(--spacing-2) var(--spacing-3); border: 1px solid var(--border-default); border-radius: var(--radius-base);"
    >
      <option value="all">All Files</option>
      <option value="available">Available Only</option>
      <option value="checked_out">Locked Only</option>
    </select>

    <select
      id="sort-select"
      style="padding: var(--spacing-2) var(--spacing-3); border: 1px solid var(--border-default); border-radius: var(--radius-base);"
    >
      <option value="name-asc">Name (A-Z)</option>
      <option value="name-desc">Name (Z-A)</option>
      <option value="status-asc">Status (A-Z)</option>
      <option value="size-desc">Size (Largest)</option>
      <option value="size-asc">Size (Smallest)</option>
    </select>
  </div>

  <div id="loading-indicator" class="hidden"><p>Loading...</p></div>
  <div id="file-list"></div>
</section>
```

**Location**: Wire up the controls in `backend/static/js/app.js`

```javascript
document.addEventListener("DOMContentLoaded", () => {
  // Wire up search
  document.getElementById("file-search").addEventListener("input", (e) => {
    store.setSearchTerm(e.target.value);
  });

  // Wire up status filter
  document.getElementById("status-filter").addEventListener("change", (e) => {
    store.setStatusFilter(e.target.value);
  });

  // Wire up sort
  document.getElementById("sort-select").addEventListener("change", (e) => {
    store.setSortBy(e.target.value);
  });

  // Subscribe to store and render
  store.subscribe((state) => {
    renderApp(state);
  });

  // Initial load
  loadFiles();
  connectWebSocket();
});

function renderApp(state) {
  // Update loading indicator
  document
    .getElementById("loading-indicator")
    .classList.toggle("hidden", !state.isLoading);

  if (state.isLoading) {
    document.getElementById("file-list").innerHTML = "";
    return;
  }

  // Get filtered and sorted files
  const filtered = store.getFilteredFiles();
  const sorted = store.getSortedFiles(filtered);

  // Render file list
  const container = document.getElementById("file-list");
  container.innerHTML = "";

  if (sorted.length === 0) {
    container.innerHTML = "<p>No files match your criteria.</p>";
  } else {
    sorted.forEach((file) => {
      const element = createFileElement(file, state.selectedFile);
      container.appendChild(element);
    });
  }

  // Render selected file panel
  renderDetailsPanel(state.selectedFile);
}

function renderDetailsPanel(selectedFile) {
  const panel = document.getElementById("details-panel");
  const content = document.getElementById("details-content");

  if (!selectedFile) {
    panel.classList.add("hidden");
    return;
  }

  panel.classList.remove("hidden");
  content.innerHTML = `
    <h3>${selectedFile.name}</h3>
    <p><strong>Status:</strong> <span class="file-status status-${
      selectedFile.status
    }">${selectedFile.status.replace("_", " ")}</span></p>
    <p><strong>Locked by:</strong> ${selectedFile.locked_by || "N/A"}</p>
    <p><strong>Size:</strong> ${(selectedFile.size_bytes / 1024).toFixed(
      2
    )} KB</p>
  `;
}
```

---

## STAGE 11: Complete Database Migration

**Location**: Refactor user management in `backend/main.py`

```python
from database import get_db
from sqlalchemy.orm import Session
import models

# REPLACE old get_user function
def get_user(username: str, db: Session):
    """Get a user from the database."""
    return db.query(models.User).filter(models.User.username == username).first()

# REPLACE old authenticate_user
def authenticate_user(username: str, password: str, db: Session):
    """Authenticate a user against the database."""
    user = get_user(username, db)
    if not user or not verify_password(password, user.password_hash):
        return None
    return user

# UPDATE login endpoint to use database
@app.post("/api/auth/login", response_model=Token)
def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db)
):
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.username, "role": user.role},
        expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}

# UPDATE get_current_user to use database
async def get_current_user(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db)
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = get_user(username, db)
    if user is None:
        raise credentials_exception

    # Convert SQLAlchemy model to Pydantic model
    return User(
        username=user.username,
        full_name=user.full_name,
        role=user.role
    )
```

**Location**: Refactor lock management in `backend/main.py`

```python
@app.post("/api/files/checkout")
async def checkout_file(
    request: FileCheckoutRequest,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    file_path = REPO_PATH / request.filename
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")

    # Check if already locked
    existing_lock = db.query(models.FileLock).filter(
        models.FileLock.filename == request.filename
    ).first()

    if existing_lock:
        raise HTTPException(
            status_code=409,
            detail=f"File is already checked out by {existing_lock.user.username}"
        )

    # Get the user's database ID
    db_user = db.query(models.User).filter(
        models.User.username == current_user.username
    ).first()

    # Create new lock
    new_lock = models.FileLock(
        filename=request.filename,
        user_id=db_user.id,
        message=request.message
    )
    db.add(new_lock)
    db.commit()

    # Invalidate cache
    redis_client.delete("pdm:files_list")

    await manager.broadcast({
        "type": "file_locked",
        "filename": request.filename,
        "user": current_user.username,
        "message": request.message
    })

    log_audit_event(current_user.username, "CHECKOUT_FILE", request.filename)

    return {"success": True, "message": "File checked out successfully"}
```

---

This supplement provides all the critical missing pieces. Each section is labeled with where it goes in relation to the tutorial stages. Use this alongside both tutorials to have a complete implementation.
