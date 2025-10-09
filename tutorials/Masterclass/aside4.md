Perfect! Let’s do **Step 3** in the same narrative, deep-explanation style we used for Steps 1 and 2, fully integrated with reasoning, “why” and “how,” without bullet points or glossary-style definitions. I’ll walk through it exactly like we did before.

---

## Step 3: Config – Loading & Saving Settings (User Preferences – 1hr)

The goal of Step 3 is to create a settings panel where users can enter their GitLab URL and personal access token. This step introduces persistent configuration: the app now remembers user preferences across sessions. After Step 2, authentication is in place, so we know who the user is. Step 3 makes the app personal for that user by storing and recalling their GitLab connection details.

### Branch Prep

Start a new branch for this step:

```bash
git checkout -b step-3-config
```

This isolates the work so we can experiment without affecting the main flow.

### 3a: Client-Side Config State

We want a single place in the app to store user preferences like the GitLab URL and token. In JavaScript, an object is perfect for this. Objects let us map keys to values: for example, `config.gitlab_url` points to `"https://gitlab.com"`, and `config.token` holds the personal token. We initialize an empty object in `ui/config.js`:

```javascript
let config = {};
```

At first, it’s empty, but later we’ll fill it with data from the server. Using an object centralizes access: anywhere in the app that needs the URL or token can read it from `config`, avoiding repeated queries or scattered variables.

To make this manageable, we define two helper functions: one for reading the current config and one for writing and persisting it. `getConfig()` returns the current object, and `setConfig(newConfig)` copies a new object into the state and stores it in `localStorage`. We use `JSON.stringify` to turn the object into a string because `localStorage` only stores strings. The spread operator ensures we make a shallow copy, preventing accidental external mutations from affecting the stored state:

```javascript
export function getConfig() {
  return config;
}

export function setConfig(newConfig) {
  config = { ...newConfig };
  localStorage.setItem("config", JSON.stringify(config));
}
```

The separation of state (`config`) and persistence (`localStorage`) follows a clean pattern: you can change one without breaking the other. This also makes debugging easier because `getConfig` always returns the authoritative state.

### 3b: Backend Config Storage

On the backend, we need to persist these preferences across server restarts. A JSON file works well here: it’s human-readable, language-independent, and simple to parse. In `backend/config.py`, we define a `CONFIG_FILE` using Python’s `pathlib`, which handles cross-platform paths safely:

```python
from pathlib import Path
import json

CONFIG_FILE = Path("config.json")
```

We create two functions: `load_config()` reads from the file, and `save_config(data)` writes to it. `load_config()` checks if the file exists. If it does, it reads the contents and parses the JSON string into a dictionary. If not, it returns an empty dictionary so the app can safely start without a config file:

```python
def load_config():
    if CONFIG_FILE.exists():
        with open(CONFIG_FILE, 'r') as f:
            return json.loads(f.read())
    return {}
```

Saving the configuration involves ensuring the directory exists, opening the file in write mode, and converting the Python dictionary to a pretty JSON string:

```python
def save_config(data):
    CONFIG_FILE.parent.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_FILE, 'w') as f:
        f.write(json.dumps(data, indent=2))
```

Using `with open()` ensures the file is properly closed after writing, preventing resource leaks. `mkdir(parents=True, exist_ok=True)` guarantees that the folder structure exists so the write doesn’t fail. Pretty-printing (`indent=2`) makes it readable if you ever want to inspect it manually.

### 3c: Client-Server Wiring

Now we connect the frontend and backend. In the UI, we add a simple form for the GitLab URL and token:

```html
<form id="configForm">
  <input
    id="gitlabUrl"
    placeholder="GitLab URL"
    class="block w-full mb-2 p-2 border rounded"
  />
  <input
    id="token"
    type="password"
    placeholder="Token"
    class="block w-full mb-2 p-2 border rounded"
  />
  <button
    data-action="saveConfig"
    type="submit"
    class="bg-green-500 text-white w-full p-2 rounded"
  >
    Save
  </button>
</form>
```

We add a “Load” button to pull the current config from the server:

```html
<button
  data-action="loadConfig"
  class="bg-gray-500 text-white px-4 py-2 rounded mb-2"
>
  Load
</button>
```

The `data-action` attributes let our main JS handle clicks through delegation rather than assigning multiple event listeners. This keeps the code clean.

In `ui/config.js`, we write a `loadConfig()` function that fetches `/config` from the backend, parses the JSON, updates `config`, and fills the form fields:

```javascript
export async function loadConfig() {
  try {
    const response = await fetch("/config");
    if (!response.ok) throw new Error(`Load failed: ${response.status}`);
    const data = await response.json();
    setConfig(data);
    document.getElementById("gitlabUrl").value = data.gitlab_url || "";
    document.getElementById("token").value = data.token || "";
    showNotification("Settings loaded");
  } catch (error) {
    console.error("Load error:", error);
    showNotification("Load failed—try again", "error");
  }
}
```

Notice how the form update is separate from the state update: `setConfig(data)` updates the centralized object, and setting `.value` updates the UI. This separation makes the app more modular.

Saving works in the opposite direction. When the user clicks “Save,” we collect all form fields into a `FormData` object and POST it to the backend:

```javascript
export async function saveConfig(form) {
  const formData = new FormData(form);
  try {
    const response = await fetch("/config/gitlab", {
      method: "POST",
      body: formData,
    });
    if (!response.ok) throw new Error("Save failed");
    await loadConfig(); // Confirm saved state
    showNotification("Saved!");
  } catch (error) {
    showNotification(error.message, "error");
  }
}
```

Using `FormData` allows the POST to automatically handle all inputs without manually building JSON. The backend parses the fields and writes them to the JSON file using the functions we defined earlier. Wrapping the fetch in try/catch ensures that network errors or server failures don’t crash the app, and the user sees clear feedback.

### Step 3 Outcome

By the end of Step 3, we have a fully functional configuration panel. Users can enter their GitLab URL and token, save them, and reload them across sessions. The frontend state is centralized in `config.js`, persistent through `localStorage`, and synced with the backend JSON file. This sets the foundation for Step 4, where we’ll list GitLab files using the saved configuration.

Git commit for this step:

```bash
git add ui/config.js main.js index.html backend/config.py
git commit -m "feat(step-3): config load/save with client-server wiring"
```

---

If you like, I can rewrite **Step 4** next in exactly the same full, narrative style with reasoning, code flow, and deep explanation.

Do you want me to do that?
