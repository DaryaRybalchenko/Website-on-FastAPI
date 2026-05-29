from __future__ import annotations
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from app.templating import get_templates
from app.routers import accounts
from app.routers import organizations
from app.routers import employees
from app.routers import units
from app.routers import products
from app.routers import customers
from app.routers import departments
from app.routers import positions
from app.routers import proxies
from app.routers import writeoff_acts
from app.database import init_db
app = FastAPI(title="Доверенности (FastAPI)")

# Используем общий экземпляр шаблонов
templates = get_templates()

# Подключаем статику
app.mount("/static", StaticFiles(directory="app/static"), name="static")

@app.on_event("startup")
async def on_startup():
    init_db()

@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

app.include_router(accounts.router, prefix="/accounts", tags=["accounts"])
app.include_router(organizations.router, prefix="/organizations", tags=["organizations"])
app.include_router(employees.router, prefix="/employees", tags=["employees"])
app.include_router(units.router, prefix="/units", tags=["units"])
app.include_router(products.router, prefix="/products", tags=["products"])
app.include_router(customers.router, prefix="/customers", tags=["customers"])
app.include_router(departments.router, prefix="/departments", tags=["departments"])
app.include_router(positions.router, prefix="/positions", tags=["positions"])
app.include_router(proxies.router, prefix="/proxies", tags=["proxies"])
app.include_router(writeoff_acts.router, prefix="/writeoff-acts", tags=["writeoff_acts"])