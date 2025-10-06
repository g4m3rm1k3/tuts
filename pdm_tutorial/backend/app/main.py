"""
Main FastAPI application entry point

This file should be thin - just app initialization and router inclusion
Business logic goes in services/, routes go in api/.
"""
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from app.config import settings
from app.api import files


def create_application() -> FastAPI:
    """
    Application factory pattern

    Benefits:
    - Can create multilpe app instances (useful for testing)
    - Configuration centralized
    - Easy to add startup/shutdown logic
    """
    app = FastAPI(title=settings.NAME, version=settings.VERSION, description="Parts Data Management System - A collaborative file locking system",
                  debug=settings.DEBUG)

    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:3000", "http://127.0.0.1:8000"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    # SECTION 2.5: Include Routers
    app.include_router(files.router)

    app.mount(
        "/static",
        StaticFiles(directory=settings.BASE_DIR / "static"),
        name="static"
    )

    @app.get("/", response_class=FileResponse, include_in_schema=False)
    async def serve_frontend():
        return FileResponse(settings.BASE_DIR / "static/index.html")

    @app.on_event("startup")
    async def startup_event():
        print(f"Starting {settings.NAME} v{settings.VERSION}")

    @app.on_event("shutdown")
    async def shutdown_event():
        print("Shutting down gracefully")

    @app.get("/")
    def read_root():
        return {
            "name": settings.NAME,
            "version": settings.VERSION,
            "status": "operational",
            "message": "Welcome to the PMD Backend API"
        }
    return app


app = create_application()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="127.0.0.1",
        port=8000,
        reload=True,
        log_level="info"
    )
