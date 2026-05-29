from __future__ import annotations
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import organizations as schemas
from ..crud import organization as crud
from ..crud import account as account_crud
from ..templating import get_templates


templates = get_templates()
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def list_organizations(request: Request, db: Session = Depends(get_db)):
    items = crud.get_organizations(db)
    return templates.TemplateResponse("organizations/list.html", {"request": request, "organizations": items})

@router.get("/create", response_class=HTMLResponse)
def create_organization_form(request: Request, db: Session = Depends(get_db)):
    accounts = account_crud.get_accounts(db)
    return templates.TemplateResponse(
        "organizations/create.html",
        {"request": request, "accounts": accounts}
    )

@router.post("/create")
def create_organization(
    name: str = Form(...),
    address: str = Form(...),
    account_id: str | None = Form(None),   # может прийти "" из <select>
    chief: str = Form(...),
    financial_chief: str = Form(...),
    db: Session = Depends(get_db),
):
    account_id_int = int(account_id) if account_id not in (None, "", "null") else None
    obj_in = schemas.OrganizationCreate(
        name=name,
        address=address,
        account_id=account_id_int,
        chief=chief,
        financial_chief=financial_chief,
    )
    crud.create_organization(db, obj_in)
    return RedirectResponse(url="/organizations", status_code=303)

@router.get("/{item_id}/edit", response_class=HTMLResponse)
def edit_organization_form(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud.get_organization(db, item_id)
    accounts = account_crud.get_accounts(db)
    return templates.TemplateResponse(
        "organizations/edit.html",
        {"request": request, "item": item, "accounts": accounts}
    )

@router.post("/{item_id}/edit")
def update_organization(
    item_id: int,
    name: str = Form(...),
    address: str = Form(...),
    account_id: str | None = Form(None),
    chief: str = Form(...),
    financial_chief: str = Form(...),
    db: Session = Depends(get_db),
):
    db_obj = crud.get_organization(db, item_id)
    account_id_int = int(account_id) if account_id not in (None, "", "null") else None
    obj_in = schemas.OrganizationUpdate(
        name=name,
        address=address,
        account_id=account_id_int,
        chief=chief,
        financial_chief=financial_chief,
    )
    crud.update_organization(db, db_obj, obj_in)
    return RedirectResponse(url="/organizations", status_code=303)

@router.get("/{item_id}/delete", response_class=HTMLResponse)
def delete_organization_form(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud.get_organization(db, item_id)
    return templates.TemplateResponse("organizations/delete.html", {"request": request, "item": item})

@router.post("/{item_id}/delete")
def delete_organization(item_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_organization(db, item_id)
    crud.delete_organization(db, db_obj)
    return RedirectResponse(url="/organizations", status_code=303)