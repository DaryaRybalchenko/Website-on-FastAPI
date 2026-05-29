from __future__ import annotations
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..schemas import products as schemas
from ..crud import product as crud
from ..crud import unit as unit_crud
from ..templating import get_templates


templates = get_templates()
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def list_products(request: Request, db: Session = Depends(get_db)):
    items = crud.get_products(db)
    return templates.TemplateResponse("products/list.html", {"request": request, "products": items})

@router.get("/create", response_class=HTMLResponse)
def create_product_form(request: Request, db: Session = Depends(get_db)):
    units = unit_crud.get_units(db)
    return templates.TemplateResponse("products/create.html", {"request": request, "units": units})

@router.post("/create")
def create_product(
    name: str = Form(...),
    price: float = Form(...),
    unit_id: int = Form(...),
    db: Session = Depends(get_db),
):
    obj_in = schemas.ProductCreate(name=name, price=price, unit_id=unit_id)
    crud.create_product(db, obj_in)
    return RedirectResponse(url="/products", status_code=303)

@router.get("/{item_id}/edit", response_class=HTMLResponse)
def edit_product_form(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud.get_product(db, item_id)
    units = unit_crud.get_units(db)
    return templates.TemplateResponse("products/edit.html", {"request": request, "item": item, "units": units})

@router.post("/{item_id}/edit")
def update_product(
    item_id: int,
    name: str = Form(...),
    price: float = Form(...),
    unit_id: int = Form(...),
    db: Session = Depends(get_db),
):
    db_obj = crud.get_product(db, item_id)
    obj_in = schemas.ProductUpdate(name=name, price=price, unit_id=unit_id)
    crud.update_product(db, db_obj, obj_in)
    return RedirectResponse(url="/products", status_code=303)

@router.get("/{item_id}/delete", response_class=HTMLResponse)
def delete_product_form(item_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud.get_product(db, item_id)
    return templates.TemplateResponse("products/delete.html", {"request": request, "item": item})

@router.post("/{item_id}/delete")
def delete_product(
    item_id: int,
    request: Request,
    db: Session = Depends(get_db),
):
    # Получаем продукт для проверки существования
    product = crud.get_product(db, item_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Передаем ID продукта в CRUD функцию
    success = crud.delete_product(db, item_id)
    
    if success:
        return RedirectResponse(url="/products", status_code=303)
    else:
        # Обработка ошибки удаления
        return templates.TemplateResponse(
            "products/delete_error.html",
            {
                "request": request,
                "product": product,
                "error_message": "Не удалось удалить продукт. Возможно, существуют связанные записи."
            }
        )
