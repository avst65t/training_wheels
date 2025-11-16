from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .core.exceptions import http_exception_handler
from .routers import ai_router
from fastapi import HTTPException

def create_app() -> FastAPI:
    app = FastAPI(title="Document Processing API", version="1.0.0")
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    app.include_router(ai_router.router)
    app.add_exception_handler(HTTPException, http_exception_handler)
    return app

app = create_app()
