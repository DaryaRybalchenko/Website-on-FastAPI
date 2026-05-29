from __future__ import annotations
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import customers as schemas
from ..crud import customer as crud
from ..templating import get_templates


templates = get_templates()
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def list_customers(request: Request, db: Session = Depends(get_db)):
    items = crud.get_customers(db)
    return templates.TemplateResponse("customers/list.html", {"request": request, "customers": items})

@router.get("/create", response_class=HTMLResponse)
def create_customer_form(request: Request):
    return templates.TemplateResponse("customers/create.html", {"request": request})

@router.post("/create")
def create_customer(
    name: str = Form(...),
    db: Session = Depends(get_db),
):
    obj_in = schemas.CustomerCreate(name=name)
    crud.create_customer(db, obj_in)
    return RedirectResponse(url="/customers", status_code=303)

@router.get("/{item_id}/edit", response_class=HTMLResponse)
def edit_customer_form(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud.get_customer(db, item_id)
    return templates.TemplateResponse("customers/edit.html", {"request": request, "item": item})

@router.post("/{item_id}/edit")
def update_customer(
    item_id: int,
    name: str = Form(...),
    db: Session = Depends(get_db),
):
    db_obj = crud.get_customer(db, item_id)
    obj_in = schemas.CustomerUpdate(name=name)
    crud.update_customer(db, db_obj, obj_in)
    return RedirectResponse(url="/customers", status_code=303)

@router.get("/{item_id}/delete", response_class=HTMLResponse)
def delete_customer_form(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud.get_customer(db, item_id)
    return templates.TemplateResponse("customers/delete.html", {"request": request, "item": item})

@router.post("/{item_id}/delete")
def delete_customer(item_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_customer(db, item_id)
    crud.delete_customer(db, db_obj)
    return RedirectResponse(url="/customers", status_code=303)