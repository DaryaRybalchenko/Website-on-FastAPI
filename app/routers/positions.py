from __future__ import annotations
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import positions as schemas
from ..crud import position as crud
from ..templating import get_templates


templates = get_templates()
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def list_positions(request: Request, db: Session = Depends(get_db)):
    items = crud.get_positions(db)
    return templates.TemplateResponse("positions/list.html", {"request": request, "positions": items})

@router.get("/create", response_class=HTMLResponse)
def create_position_form(request: Request):
    return templates.TemplateResponse("positions/create.html", {"request": request})

@router.post("/create")
def create_position(name: str = Form(...), db: Session = Depends(get_db)):
    obj_in = schemas.PositionCreate(name=name)
    crud.create_position(db, obj_in)
    return RedirectResponse(url="/positions", status_code=303)

@router.get("/{item_id}/edit", response_class=HTMLResponse)
def edit_position_form(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud.get_position(db, item_id)
    return templates.TemplateResponse("positions/edit.html", {"request": request, "item": item})

@router.post("/{item_id}/edit")
def update_position(item_id: int, name: str = Form(...), db: Session = Depends(get_db)):
    db_obj = crud.get_position(db, item_id)
    obj_in = schemas.PositionUpdate(name=name)
    crud.update_position(db, db_obj, obj_in)
    return RedirectResponse(url="/positions", status_code=303)

@router.get("/{item_id}/delete", response_class=HTMLResponse)
def delete_position_form(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud.get_position(db, item_id)
    return templates.TemplateResponse("positions/delete.html", {"request": request, "item": item})

@router.post("/{item_id}/delete")
def delete_position(item_id: int, db: Session = Depends(get_db)):
    db_obj = crud.get_position(db, item_id)
    crud.delete_position(db, db_obj)
    return RedirectResponse(url="/positions", status_code=303)