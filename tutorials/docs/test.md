## **Section 1.5 `files.py` – File Management API Endpoints**

**Goal:**
Understand how to define **API routes in FastAPI**, return **typed responses**, and structure a backend for maintainability. This file is intentionally **thin**, focusing on **route definitions only**, leaving business logic for later (services/ stage).

---

### **SECTION 1: Router Setup**

```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/api/files",
    tags=["files"],
)
```

**Key Points:**

1. **`APIRouter`**:

   - Modular way to define endpoints separate from the main app.
   - Promotes **separation of concerns**, making code **scalable and testable**.

2. **`prefix="/api/files"`**:

   - All routes in this router will be prefixed automatically.
   - E.g., `GET /api/files/` instead of repeating the path in every endpoint.

3. **`tags=["files"]`**:

   - Groups routes in **OpenAPI documentation**.
   - Improves developer experience for anyone using Swagger UI or Redoc.

**Software Engineering Insight:**

- Using routers is a **common pattern in backend frameworks** (like Flask Blueprints or Django apps) to avoid **monolithic code**.
- Encourages **modularity and maintainability**, which is key in real-world software projects.

---

### **SECTION 2: Hardcoded Data (Temporary)**

```python
MOCK_FILES = [
    {"name": "PN1001_OP1.mcam", "status": "available", "size_bytes": 1234567, "locked_by": None},
    {"name": "PN1002_OP1.mcam", "status": "checked_out", "size_bytes": 2345678, "locked_by": "john"},
    {"name": "PN1003_OP1.mcam", "status": "available", "size_bytes": 987654, "locked_by": None}
]
```

**Key Points:**

1. **Temporary hardcoded data** is useful for:

   - **Prototyping endpoints** before implementing actual services
   - Ensuring **API contracts** are working and returning correct types

2. **`locked_by` as `None`** → consistent with `Optional[str]` in Pydantic schemas

**CS Insight:**

- Using mock data is a **standard practice in Test-Driven Development (TDD)**: write your tests/routes before connecting to the database.
- Separates **API behavior** from **business logic**, making incremental development smoother.

---

### **SECTION 3: GET Endpoints**

#### **Get all files**

```python
@router.get("/", response_model=FileListResponse)
def get_files():
    return FileListResponse(files=MOCK_FILES, total=len(MOCK_FILES))
```

**Key Points:**

1. **`@router.get("/")`** → HTTP GET method

2. **`response_model=FileListResponse`**:

   - FastAPI **validates the returned object** against the model
   - Automatically generates **OpenAPI docs**
   - Ensures the frontend **always gets the expected structure**

3. **Return object** is **typed**:

   ```python
   FileListResponse(files=MOCK_FILES, total=len(MOCK_FILES))
   ```

**Software Engineering Insight:**

- Typed responses **reduce runtime errors** and **improve developer confidence**
- This aligns with **interface segregation principle**: the endpoint only exposes what it needs to.

---

#### **Get a single file**

```python
@router.get("/{filename}", response_model=FileInfo)
def get_file(filename: str):
    for file in MOCK_FILES:
        if file["name"] == filename:
            return FileInfo(**file)

    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND,
        detail=f"File '{filename}' not found"
    )
```

**Key Points:**

1. **Path parameter `{filename}`**:

   - Passed as a function argument
   - FastAPI automatically converts and validates it as a `str`

2. **Data validation**:

   - `FileInfo(**file)` → ensures mock data conforms to Pydantic model

3. **Error handling**:

   - `HTTPException` with `status_code` and `detail` ensures **RESTful error reporting**
   - FastAPI automatically serializes this to JSON

**CS Insight:**

- Separating **normal flow** vs **exceptional flow** is a core principle of robust backend design.
- Consistent **HTTP status codes** improve API usability and make integrations predictable.

---

### **SECTION 4: Placeholder Endpoints**

```python
@router.post("/checkout")
def checkout_file():
    return {"message": "Checkout endpoint - coming in Stage 3"}

@router.post("/checkin")
def checkin_file():
    return {"message": "Checkin endpoint - coming in Stage 3"}
```

**Key Points:**

1. These endpoints are **stubs**:

   - Defined now to complete the **API contract**
   - Implementation comes later in **services/**

2. **Why placeholders?**

   - Allows **frontend development** to start
   - Enables **integration testing** without full backend logic
   - Encourages **iterative development** (Agile principle)

---

### ✅ **Key Takeaways from `files.py`**

1. **Routers modularize endpoints**, keeping main app clean
2. **Response models enforce type safety** and **generate docs** automatically
3. **Path parameters + validation** ensure endpoints are robust and predictable
4. **Mock data** allows early-stage testing before implementing business logic
5. **Placeholder endpoints** help maintain a **working API contract** for frontend/backend integration
6. **Error handling via HTTPException** is crucial for **RESTful API design**

---

**CS & SE Insight Recap:**

- **Modularity** → `APIRouter` promotes separation of concerns
- **Type safety** → Pydantic models enforce contracts at runtime
- **Iterative development** → mock data + stubs enable early testing and frontend integration
- **Error handling** → clear and predictable API responses
- **Documentation** → auto-generated OpenAPI docs improve developer experience
