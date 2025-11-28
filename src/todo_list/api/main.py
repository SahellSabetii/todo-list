from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routers import api_router


def create_application() -> FastAPI:
    app = FastAPI(
        title="TodoList API",
        description="A sophisticated TodoList application with PostgreSQL and FastAPI",
        version="1.0.0",
        docs_url="/docs",
        redoc_url="/redoc",
        openapi_url="/openapi.json"
    )
    
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    app.include_router(api_router, prefix="/api/v1")
    
    @app.get("/health", tags=["health"])
    async def health_check():
        return {"status": "healthy", "message": "TodoList API is running"}
    
    @app.get("/", tags=["root"])
    async def root():
        return {
            "message": "Welcome to TodoList API",
            "version": "1.0.0",
            "docs": "/docs",
            "health": "/health"
        }
    
    return app


app = create_application()
