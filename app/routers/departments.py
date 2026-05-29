from __future__ import annotations
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import departments as schemas
from ..crud import department as crud
from ..templating import get_templates


templates = get_templates()
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def list_departments(request: Request, db: Session = Depends(get_db)):
    items = crud.get_departments(db)
    return templates.TemplateResponse("departments/list.html", {"request": request, "departments": items})

@router.get("/create", response_class=HTMLResponse)
def create_department_form(request: Request):
    return templates.TemplateResponse("departments/create.html", {"request": request})

@router.post("/create")
def create_department(name: str = Form(...), db: Session = Depends(get_db)):
    obj_in = schemas.DepartmentCreate(name=name)
    crud.create_department(db, obj_in)
    return RedirectResponse(url="/departments", status_code=303)

@router.get("/{item_id}/edit", response_class=HTMLResponse)
def edit_department_form(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud.get_department(db, item_id)
    return templates.TemplateResponse("departments/edit.html", {"request": request, "item": item})

@router.post("/{item_id}/edit")
def update_department(item_id: int, name: str = Form(...), db: Session = Depends(get_db)):
    db_obj = crud.get_department(db, item_id)
    obj_in = schemas.DepartmentUpdate(name=name)
    crud.update_department(db, db_obj, obj_in)
    return RedirectResponse(url="/departments", status_code=303)

@router.get("/{item_id}/delete", response_class=HTMLResponse)
def delete_department_form(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud.get_department(db, item_id)
    return templates.TemplateResponse("departments/delete.html", {"request": request, "item": item})

@router.post("/{item_id}/delete")
def delete_department(item_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_department(db, item_id)
    crud.delete_department(db, db_obj)
    return RedirectResponse(url="/departments", status_code=303)