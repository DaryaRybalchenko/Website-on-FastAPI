# app/routers/accounts.py
from __future__ import annotations
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import accounts as schemas
from ..crud import account as crud
from ..templating import get_templates


templates = get_templates()
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def list_accounts(request: Request, db: Session = Depends(get_db)):
    items = crud.get_accounts(db)
    return templates.TemplateResponse("accounts/list.html", {"request": request, "accounts": items})

@router.get("/create", response_class=HTMLResponse)
def create_account_form(request: Request):
    return templates.TemplateResponse("accounts/create.html", {"request": request})

@router.post("/create")
def create_account(
    account: str = Form(...),
    bank_name: str = Form(...),
    bank_identity_number: str = Form(...),
    db: Session = Depends(get_db),
):
    obj_in = schemas.AccountCreate(
        account=account,
        bank_name=bank_name,
        bank_identity_number=bank_identity_number,
    )
    crud.create_account(db, obj_in)
    return RedirectResponse(url="/accounts", status_code=303)

@router.get("/{item_id}/edit", response_class=HTMLResponse)
def edit_account_form(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud.get_account(db, item_id)
    return templates.TemplateResponse("accounts/edit.html", {"request": request, "item": item})

@router.post("/{item_id}/edit")
def update_account(
    item_id: int,
    account: str = Form(...),
    bank_name: str = Form(...),
    bank_identity_number: str = Form(...),
    db: Session = Depends(get_db),
):
    db_obj = crud.get_account(db, item_id)
    obj_in = schemas.AccountUpdate(
        account=account,
        bank_name=bank_name,
        bank_identity_number=bank_identity_number,
    )
    crud.update_account(db, db_obj, obj_in)
    return RedirectResponse(url="/accounts", status_code=303)

@router.get("/{item_id}/delete", response_class=HTMLResponse)
def delete_account_form(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud.get_account(db, item_id)
    return templates.TemplateResponse("accounts/delete.html", {"request": request, "item": item})

@router.post("/{item_id}/delete")
def delete_account(item_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_account(db, item_id)
    crud.delete_account(db, db_obj)
    return RedirectResponse(url="/accounts", status_code=303)