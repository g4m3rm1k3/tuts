Of course. Let's begin the final major architectural upgrade for our application.

We have a powerful Git engine for versioning and a sleek API. But where do we store data _about_ our files, like user-friendly descriptions? Putting this in Git would mean creating a new commit just to fix a typo in a description, which is inefficient. The professional solution is to use a database for metadata.

This part will introduce you to **SQLAlchemy**, Python's most powerful **Object-Relational Mapper (ORM)**, and integrate it seamlessly into our FastAPI application.

---

### **Part 11: Making It Permanent - Database Integration (Masterclass Edition)**

#### **🚩 Step 1: What is an ORM?**

An **Object-Relational Mapper** is a library that acts as a translator between your programming language's objects (like Python classes) and a relational database's tables.

- **The Problem**: Python thinks in objects, but a SQL database thinks in tables, rows, and columns. Writing raw SQL queries as strings in your Python code is error-prone, hard to maintain, and can be insecure.
- **The Solution**: An ORM like SQLAlchemy lets you interact with your database using pure Python code. You define a Python class, and the ORM automatically maps it to a database table. You call Python methods, and the ORM generates the safe, efficient SQL for you. .

🔑 **Transferable Skill**: The ORM is a dominant pattern in modern software. Learning SQLAlchemy teaches you concepts directly applicable to other popular ORMs like Django's ORM, Ruby on Rails' Active Record, Java's Hibernate, and Prisma in the JavaScript world.

---

#### **🚩 Step 2: Setup and Installation**

Because FastAPI is an asynchronous framework, we need to install SQLAlchemy along with a compatible async database driver. **SQLite** is a simple, file-based database perfect for our needs.

1.  **Install Libraries**: In your `backend` directory with `(venv)` active:

    ```bash
    pip install "sqlalchemy[aiosqlite]"
    pip freeze > requirements.txt
    ```

2.  **Create the Database Module**: This is the central point for all database connection logic. Create `backend/database.py`:

    ```python
    # backend/database.py
    from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
    from sqlalchemy.orm import declarative_base

    DATABASE_URL = "sqlite+aiosqlite:///./vcs_app.db"

    engine = create_async_engine(DATABASE_URL, connect_args={"check_same_thread": False})
    SessionLocal = async_sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base = declarative_base()
    ```

---

#### **🚩 Step 3: The Database Model**

Just as we created a Pydantic model for our API, we'll now create a SQLAlchemy model for our database table.

Create `backend/models/file_meta.py`:

```python
# backend/models/file_meta.py
from sqlalchemy import Column, String
from database import Base

class FileMeta(Base):
    __tablename__ = "file_metadata"

    filename = Column(String, primary_key=True, index=True)
    description = Column(String, nullable=True)
```

🔎 **Deep Explanation**: This class defines a table named `file_metadata` with two columns. `filename` is the **primary key**, meaning it's the unique identifier for each row. The `description` is a simple string that can be null. SQLAlchemy will use this class definition to generate the `CREATE TABLE` SQL command.

---

#### **🚩 Step 4: The CRUD Layer**

To keep our logic clean, we'll create a dedicated file for all database operations, often called a CRUD (Create, Read, Update, Delete) layer.

Create `backend/crud.py`:

```python
# backend/crud.py
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from models.file_meta import FileMeta

async def get_description(db: AsyncSession, filename: str) -> str | None:
    result = await db.execute(select(FileMeta).filter(FileMeta.filename == filename))
    db_file = result.scalars().first()
    return db_file.description if db_file else "No description set."

async def update_description(db: AsyncSession, filename: str, description: str):
    result = await db.execute(select(FileMeta).filter(FileMeta.filename == filename))
    db_file = result.scalars().first()
    if not db_file:
        db_file = FileMeta(filename=filename)
        db.add(db_file)

    db_file.description = description
    await db.commit()
    await db.refresh(db_file)
    return db_file
```

---

#### **🚩 Step 5: Integrating DB into the API (`main.py`)**

This is the most critical step. How do our API endpoints get a database session to work with? FastAPI uses a powerful **Dependency Injection** pattern.

Update `backend/main.py`:

```python
# backend/main.py

# 1. Imports
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from database import engine, SessionLocal, Base
from models import file_meta, history # Ensure models are imported
from crud import update_description # Import our new crud function

# 2. Add startup/shutdown events to create the DB table
@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        # await conn.run_sync(Base.metadata.drop_all) # Use this to reset DB
        await conn.run_sync(Base.metadata.create_all)

# 3. Create the database dependency
async def get_db():
    async with SessionLocal() as session:
        yield session

# 4. Update an endpoint to use the dependency
@app.get("/api/files", response_model=List[File])
async def list_files(db: AsyncSession = Depends(get_db)):
    # The endpoint now automatically gets a DB session!
    return await git_service.get_all_files(db=db)

# 5. Add the NEW endpoint for updating descriptions
class DescriptionUpdate(BaseModel):
    description: str

@app.put("/api/files/{filename}", response_model=File)
async def update_file_description(
    filename: str,
    desc_update: DescriptionUpdate,
    db: AsyncSession = Depends(get_db)
):
    await update_description(db, filename, desc_update.description)
    return await git_service.get_file_details(filename, db)

# ... (you will need to update all other endpoints to accept and pass the `db` session) ...
```

---

#### **🚩 Step 6: Updating the Service Layer**

Our `git_service.py` now needs to be aware of the database to fetch descriptions.

Update `backend/services/git_service.py`:

```python
# backend/services/git_service.py
from sqlalchemy.ext.asyncio import AsyncSession
from crud import get_description

# Update the helper function to accept a db session
def _get_file_details(filename: str, description: str):
    # ... (logic to get status, revision etc. from git) ...
    return {
        "filename": filename,
        "description": description, # Use the description passed from the DB
        # ... (rest of the fields)
    }

# Update the main function to fetch from both git and db
async def get_all_files(db: AsyncSession):
    files = []
    # ... (loop through git files) ...
        # For each file, fetch its description from the DB
        desc = await get_description(db, item.path)
        files.append(await _get_file_details(item.path, db))
    return files

# You must refactor all other service functions to accept and use the `db` session.
```

---

#### **✅ Recap**

This was a dense but incredibly powerful architectural upgrade. You've now built a hybrid system that uses the best tool for each job: Git for file versioning and a SQL database for structured metadata.

You have learned:

- The role and benefit of an **Object-Relational Mapper (ORM)**.
- How to define database tables as Python classes with **SQLAlchemy**.
- To separate database logic into a **CRUD layer**.
- The professional pattern for managing database connections in FastAPI using **Dependency Injection**.
- How to combine data from multiple sources (Git and a database) into a single API response.

#### **📌 What's Next:**

The architecture of our application is now complete and professional. The foundation is rock-solid. All that remains is to build on top of it. In the final modules, we'll cover the essential topics for making this app truly production-ready: **Authentication**, **WebSockets**, **Testing**, and **Deployment**.
