from fastapi import FastAPI

from app.api.routes_invoices import router as invoices_router

app = FastAPI(
    title="Notax API",
    description="API for validation of tax documents.",
    version="1.0.0"
)

app.include_router(invoices_router)

@app.get("/")
def read_root():
    return {"message": "Notax API is running!"}

@app.get("/health")
def read_health():
    return {"status": "ok"}

