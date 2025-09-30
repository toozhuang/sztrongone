from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.db import create_db_and_tables
from app.routers.health import router as health_router
from app.routers.institutions import router as institutions_router
from app.routers.accounts import router as accounts_router
from app.routers.deposit_products import router as deposit_products_router
from app.routers.deposits import router as deposits_router
from app.routers.maturity_reminders import router as maturity_reminders_router
from app.routers.files import router as files_router
from app.routers.ocr import router as ocr_router
from app.routers.ocr_templates import router as ocr_templates_router
from app.routers.deposit_drafts import router as deposit_drafts_router
from app.routers.reports import router as reports_router

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
app.include_router(accounts_router, prefix="/accounts", tags=["accounts"])
app.include_router(deposit_products_router, prefix="/deposit-products", tags=["deposit_products"])
app.include_router(deposits_router, prefix="/deposits", tags=["deposits"])
app.include_router(maturity_reminders_router, prefix="/maturity-reminders", tags=["maturity_reminders"])
app.include_router(files_router, prefix="/files", tags=["files"])
app.include_router(ocr_router, prefix="/ocr", tags=["ocr"])
app.include_router(ocr_templates_router, prefix="/ocr/templates", tags=["ocr_templates"])
app.include_router(deposit_drafts_router, prefix="/deposit-drafts", tags=["deposit_drafts"])
app.include_router(reports_router, prefix="/reports", tags=["reports"])
