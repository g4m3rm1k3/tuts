Excellent. Let's proceed with Part 2A. We'll build the next logical piece of our API: an endpoint to retrieve a _single_, specific file.

This will introduce two more cornerstone concepts of professional API development: **path parameters** and **error handling**.

---

### **Part 2A: Fetching Single Items & Handling Errors (Masterclass Edition)**

We've built an endpoint that returns a list of all files. Now, a user needs to view the details of just one. We need a way to tell our API, "Don't give me everything, just give me the file named `project_beta.vnc`."

This is where path parameters come in.

---

#### **🚩 Step 1: The Concept - Path Parameters**

A **path parameter** is a variable part of a URL path. It's used to identify a specific resource.

Think of the URL as an address:

- `/api/files`: This is like asking for the address of an entire apartment building. You get a list of all the units.
- `/api/files/{filename}`: This is like asking for a specific unit, like "Apartment **3B**". The `3B` part is the parameter that identifies the exact resource you want.

We use curly braces `{}` to denote a path parameter. FastAPI will capture the value from that segment of the URL and pass it into our function.

🔑 **Transferable Skill:** This is a fundamental pattern in **REST (Representational State Transfer)**, the architectural style that governs how most modern APIs are designed. You see it everywhere:

- `https://api.github.com/users/{username}`
- `https://api.spotify.com/v1/artists/{id}`
  The concept of using the URL to uniquely identify a resource is universal.

---

#### **🚩 Step 2: Implementing the Single-File Endpoint**

Let's add the new endpoint to our `backend/main.py` file.

```python
# backend/main.py

# Add HTTPException to our imports
from fastapi import FastAPI, HTTPException
from typing import List
from models.file import File
from db import mock_db

app = FastAPI()

@app.get("/api/files", response_model=List[File])
async def list_files():
    """
    Returns a list of all version-controlled files.
    """
    return mock_db["files"]

# --- NEW ENDPOINT ---
@app.get("/api/files/{filename}", response_model=File)
async def get_file(filename: str):
    """
    Retrieves the details of a single file by its name.
    """
    # Find the file in our mock database
    for file in mock_db["files"]:
        if file["filename"] == filename:
            return file

    # If the loop finishes and we haven't found the file, raise an error
    raise HTTPException(status_code=404, detail="File not found")

```

🔎 **Deep Explanation**

- `@app.get("/api/files/{filename}", ...)`: We define the new route. FastAPI understands that `{filename}` is a placeholder.
- `async def get_file(filename: str):`: Look at the function signature. We have a parameter `filename` with the type `str`. FastAPI is smart: it automatically sees that the name in the path `{filename}` matches the argument name `filename` and passes the value from the URL directly into your function.
- **The Logic:** We loop through our list of files. If we find a match, we return it immediately.

---

#### **🚩 Step 3: The Reality - Graceful Error Handling**

What happens if a user asks for a file that doesn't exist?

Without the last line of code, our function would finish the loop, find nothing, and implicitly return `None`. FastAPI would then try to validate `None` against our `response_model=File`, which would fail and result in a generic, ugly **`500 Internal Server Error`**. This is a bad user experience and tells the client nothing about _what_ went wrong.

A professional API must give clear, meaningful error messages.

- `raise HTTPException(...)`: This is FastAPI's built-in way to stop execution and immediately send a specific HTTP error response back to the client.
- `status_code=404`: This is the standard HTTP status code for **"Not Found."** Using correct status codes is critical because it allows frontend applications to programmatically handle different outcomes. For example, `if response.status == 404: show_error_message()`.
- `detail="File not found"`: This provides a human-readable JSON message explaining the error.

🔑 **Transferable Skill:** Proper error handling and the use of correct HTTP status codes are non-negotiable skills for a backend developer. An API that returns `500` for a simple "not found" error is considered broken. Common codes include:

- **200 OK:** Everything worked.
- **201 Created:** A new resource was successfully created.
- **400 Bad Request:** The user sent invalid data (e.g., a malformed JSON).
- **401 Unauthorized:** The user isn't logged in.
- **403 Forbidden:** The user is logged in but doesn't have permission to do this.
- **404 Not Found:** The requested resource doesn't exist.

---

#### **🚩 Step 4: Testing the Good and Bad Paths**

Make sure your `uvicorn` server is running. Now, let's test both possible outcomes.

1.  **The "Happy Path":**
    Open your browser and go to a URL for a file that _does_ exist:
    `http://127.0.0.1:8000/api/files/project_beta.vnc`
    You should see the single, clean JSON object for that file.

2.  **The "Error Path":**
    Now, go to a URL for a file that _does not_ exist:
    `http://127.0.0.1:8000/api/files/this_file_is_fake.txt`
    You should see the clean, helpful 404 error response:
    `{"detail":"File not found"}`

3.  **Check The Docs:**
    Finally, refresh your documentation page at `http://127.0.0.1:8000/docs`. Expand the new `GET /api/files/{filename}` endpoint. You'll see that FastAPI has automatically documented:

    - The `filename` path parameter, marking it as required.
    - The **"Successful Response" (Code 200)**, showing the `File` schema.
    - The **"Error Response" (Code 422)**, for validation errors and a **(Code 404)** response if the file is not found.

This is the power of a modern framework—your code, logic, and documentation all stay perfectly in sync.

---

#### **✅ Recap**

In this section, we've added a significant layer of professionalism to our API. You've learned:

- How to use **path parameters** to create endpoints for specific resources.
- The critical importance of **graceful error handling**.
- How to use `HTTPException` to return meaningful **HTTP status codes**.
- How FastAPI automatically documents both path parameters and error responses.

#### **📌 What's Next:**

We can read all files and we can read one file. The next logical step in building a full CRUD (Create, Read, Update, Delete) API is the "Create" part. In the next section, we will build an endpoint that allows a client to send data _to_ our server to create a new file, introducing us to **`POST` requests** and handling **request bodies**.
