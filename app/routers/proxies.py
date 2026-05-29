from __future__ import annotations
from typing import List
from fastapi import APIRouter, Depends, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..templating import get_templates
from ..crud import proxy as crud_proxy
from ..crud import organization as crud_org
from ..crud import employee as crud_emp
from ..crud import customer as crud_cus
from ..crud import product as crud_prod
from ..schemas.proxies import ProxyCreate, ProxyUpdate, ProxyItemCreate
from fastapi.responses import HTMLResponse, RedirectResponse


templates = get_templates()
router = APIRouter()

@router.get("/", response_class=HTMLResponse)
def list_proxies(request: Request, db: Session = Depends(get_db)):
    items = crud_proxy.get_proxies(db)
    return templates.TemplateResponse("proxies/list.html", {"request": request, "proxies": items})

@router.get("/create", response_class=HTMLResponse)
def create_proxy_form(request: Request, db: Session = Depends(get_db)):
    orgs = crud_org.get_organizations(db)
    emps = crud_emp.get_employees(db)
    custs = crud_cus.get_customers(db)
    prods = crud_prod.get_products(db)
    return templates.TemplateResponse(
        "proxies/create.html",
        {"request": request, "orgs": orgs, "emps": emps, "custs": custs, "prods": prods}
    )

@router.post("/create")
def create_proxy(
    organization_id: int = Form(...),
    employee_id: int = Form(...),
    customer_id: int = Form(...),
    date_of_issue: str = Form(...),
    is_valid_until: str = Form(...),
    product_id: List[int] = Form([]),
    amount: List[int] = Form([]),
    db: Session = Depends(get_db),
):
    items = []
    for pid, qty in zip(product_id, amount):
        if str(pid).strip() == "" or str(qty).strip() == "":
            continue
        items.append(ProxyItemCreate(product_id=int(pid), amount=int(qty)))

    obj_in = ProxyCreate(
        organization_id=organization_id,
        employee_id=employee_id,
        customer_id=customer_id,
        date_of_issue=date_of_issue,
        is_valid_until=is_valid_until,
        items=items,
    )
    crud_proxy.create_proxy(db, obj_in)
    return RedirectResponse(url="/proxies", status_code=303)

@router.get("/{proxy_id}", response_class=HTMLResponse)
def proxy_detail(proxy_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud_proxy.get_proxy(db, proxy_id)
    return templates.TemplateResponse("proxies/view.html", {"request": request, "proxy": item})

@router.get("/{proxy_id}/edit", response_class=HTMLResponse)
def edit_proxy_form(proxy_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud_proxy.get_proxy(db, proxy_id)
    orgs = crud_org.get_organizations(db)
    emps = crud_emp.get_employees(db)
    custs = crud_cus.get_customers(db)
    prods = crud_prod.get_products(db)
    return templates.TemplateResponse(
        "proxies/edit.html",
        {"request": request, "proxy": item, "orgs": orgs, "emps": emps, "custs": custs, "prods": prods}
    )

@router.post("/{proxy_id}/edit")
def update_proxy(
    proxy_id: int,
    organization_id: int = Form(...),
    employee_id: int = Form(...),
    customer_id: int = Form(...),
    date_of_issue: str = Form(...),
    is_valid_until: str = Form(...),
    product_id: List[int] = Form([]),
    amount: List[int] = Form([]),
    db: Session = Depends(get_db),
):
    items = []
    for pid, qty in zip(product_id, amount):
        if str(pid).strip() == "" or str(qty).strip() == "":
            continue
        items.append(ProxyItemCreate(product_id=int(pid), amount=int(qty)))

    obj_in = ProxyUpdate(
        organization_id=organization_id,
        employee_id=employee_id,
        customer_id=customer_id,
        date_of_issue=date_of_issue,
        is_valid_until=is_valid_until,
        items=items,
    )
    db_obj = crud_proxy.get_proxy(db, proxy_id)
    crud_proxy.update_proxy(db, db_obj, obj_in)
    return RedirectResponse(url="/proxies", status_code=303)

@router.get("/{proxy_id}/print", response_class=HTMLResponse)
def proxy_print(proxy_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud_proxy.get_proxy(db, proxy_id)
    return templates.TemplateResponse("proxies/print.html", {"request": request, "proxy": item})


@router.get("/{proxy_id}/delete", response_class=HTMLResponse)
def delete_proxy_form(proxy_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud_proxy.get_proxy(db, proxy_id)
    return templates.TemplateResponse("proxies/delete.html", {"request": request, "proxy": item})

@router.post("/{proxy_id}/delete")
def delete_proxy(proxy_id: int, db: Session = Depends(get_db)):
    db_obj = crud_proxy.get_proxy(db, proxy_id)
    crud_proxy.delete_proxy(db, db_obj)
    return RedirectResponse(url="/proxies", status_code=303)