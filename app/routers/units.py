from __future__ import annotations
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import units as schemas
from ..crud import unit as crud
from ..templating import get_templates


templates = get_templates()
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def list_units(request: Request, db: Session = Depends(get_db)):
    items = crud.get_units(db)
    return templates.TemplateResponse("units/list.html", {"request": request, "units": items})

@router.get("/create", response_class=HTMLResponse)
def create_unit_form(request: Request):
    return templates.TemplateResponse("units/create.html", {"request": request})

@router.post("/create")
def create_unit(name: str = Form(...), db: Session = Depends(get_db)):
    obj_in = schemas.UnitCreate(name=name)
    crud.create_unit(db, obj_in)
    return RedirectResponse(url="/units", status_code=303)

@router.get("/{item_id}/edit", response_class=HTMLResponse)
def edit_unit_form(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud.get_unit(db, item_id)
    return templates.TemplateResponse("units/edit.html", {"request": request, "item": item})

@router.post("/{item_id}/edit")
def update_unit(item_id: int, name: str = Form(...), db: Session = Depends(get_db)):
    db_obj = crud.get_unit(db, item_id)
    obj_in = schemas.UnitUpdate(name=name)
    crud.update_unit(db, db_obj, obj_in)
    return RedirectResponse(url="/units", status_code=303)

@router.get("/{item_id}/delete", response_class=HTMLResponse)
def delete_unit_form(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud.get_unit(db, item_id)
    return templates.TemplateResponse("units/delete.html", {"request": request, "item": item})

@router.post("/{item_id}/delete")
def delete_unit(item_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_unit(db, item_id)
    crud.delete_unit(db, db_obj)
    return RedirectResponse(url="/units", status_code=303)