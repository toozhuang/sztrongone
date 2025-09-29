from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import create_db_and_tables
from app.routers.institutions import router as institutions_router
from app.routers.health import router as health_router
from app.routers.files import router as files_router
from app.routers.ocr import router as ocr_router

app = FastAPI(title="Home Assets API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup() -> None:
    create_db_and_tables()

app.include_router(health_router, prefix="")
app.include_router(institutions_router, prefix="/institutions", tags=["institutions"])
app.include_router(files_router, prefix="/files", tags=["files"])
app.include_router(ocr_router, prefix="/ocr", tags=["ocr"])
