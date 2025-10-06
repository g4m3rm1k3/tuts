## **Section 1.3 (Part 2): FastAPI Application Initialization – Tutorial Version**

**Goal:**
Understand how to properly structure a **FastAPI backend**, why we use an **application factory**, middleware, startup/shutdown events, and separation of concerns. We’ll include **CS/software engineering insights** and **Python best practices**.

---

### **SECTION 1: Application Factory Pattern**

```python
def create_application() -> FastAPI:
```

- **Purpose:** Encapsulates **app creation logic** in a function rather than at module level
- Returns a **FastAPI instance**
- This pattern is widely used in **Flask**, **FastAPI**, and **other Python frameworks**

#### **Benefits**

1. **Multiple instances** → useful for testing:

   - You can spin up a separate app instance for **unit tests** without interfering with your main app.

2. **Centralized configuration** → app settings come from `settings` object
3. **Startup/shutdown hooks** → easy to attach lifecycle events

**Software Engineering Insight:**

- Using an application factory follows **modular design principles**
- Promotes **decoupling** and **testability**, critical in professional backend systems

---

### **SECTION 2: Middleware Configuration**

```python
from fastapi.middleware.cors import CORSMiddleware

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
```

#### **Why middleware?**

- Middleware intercepts requests/responses **before and after hitting routes**
- Common uses: **CORS, authentication, logging, error handling**

#### **CORS Explained (Cross-Origin Resource Sharing)**

- Browsers enforce the **Same-Origin Policy**: JavaScript can’t call APIs on a different domain by default
- CORS headers **tell the browser which origins are allowed**
- In production, only allow your **frontend domain** for security

**CS Concept:**

- Middleware demonstrates **intercepting layers** → a classic **pipeline pattern** in software engineering
- Allows cross-cutting concerns without polluting business logic

---

### **SECTION 3: Startup and Shutdown Events**

```python
@app.on_event("startup")
async def startup_event():
    print(f"Starting {settings.APP_NAME} v{settings.APP_VERSION}")
```

- **Startup events**: run once **when the server starts**
- Good for:

  - Connecting to databases
  - Loading caches
  - Logging server info

```python
@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down gracefully...")
```

- **Shutdown events**: run once **when the server stops**
- Good for:

  - Closing DB connections
  - Flushing logs
  - Cleanup tasks

**Python/CS Concept:**

- ASGI allows **async startup/shutdown** → non-blocking operations
- Mimics **resource management patterns** in OS-level programming

---

### **SECTION 4: Root Route (Health Check)**

```python
@app.get("/")
def read_root():
    return {
        "name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "status": "operational",
        "message": "Welcome to the PDM Backend API"
    }
```

- Simple **GET endpoint** to check server health and API metadata
- **Best practice:** every API should have a **root or health check route**

**Software Engineering Insight:**

- Useful for **monitoring tools** or load balancers
- Communicates **version and operational status** → key for CI/CD pipelines

---

### **SECTION 5: Create App Instance**

```python
app = create_application()
```

- Calls the **factory** to create a **singleton FastAPI instance**
- Other modules import `app` for **routing, middleware, and testing**

**CS Concept:**

- Follows **dependency injection principles**: app configuration is **externalized** and **passed in**, improving flexibility

---

### **SECTION 6: Development Server Entry Point**

```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
```

#### **Key points**

- `__name__ == "__main__"` → standard Python idiom to run **module as script**
- `uvicorn.run()` → launches **ASGI server**
- `reload=True` → **auto-reload** in development (not for production)
- `log_level="info"` → controls verbosity for debugging

**Best practice:**

- **Keep entry point thin** → all **business logic** belongs in `services/` or `routes/`
- **Separation of concerns** → easier maintenance and testing

**JavaScript Parallel:**

- Node/Express apps often use:

```javascript
const app = require("./app");
app.listen(3000, () => console.log("Server running"));
```

- Same idea: thin entry point, main logic elsewhere

---

### ✅ **Key Takeaways**

1. **Application Factory Pattern** → promotes modularity, testability, and centralized configuration
2. **Middleware** → intercept requests/responses for cross-cutting concerns
3. **Startup/Shutdown hooks** → manage resources reliably
4. **Root route** → health check & API metadata, best practice for monitoring
5. **Thin entry point** → separates server bootstrap from business logic
6. **CS/Software Engineering Concepts:**

   - Modular design & separation of concerns
   - Pipeline pattern (middleware)
   - Dependency injection & singleton instance
   - Resource lifecycle management

---

This structure sets you up for **scaling your app**, **testing endpoints**, and integrating **business logic in services and routes**.
