from __future__ import annotations
from typing import List
from fastapi import APIRouter, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from sqlalchemy.orm import Session
from ..database import get_db
from ..templating import get_templates
from ..crud import writeoff_act as crud_writeoff
from ..crud import organization as crud_org
from ..crud import employee as crud_emp
from ..crud import department as crud_dept
from ..crud import product as crud_prod
from ..schemas.writeoff_acts import WriteOffActCreate, WriteOffActUpdate, WriteOffActItemCreate

templates = get_templates()
router = APIRouter() 
@router.get("/", response_class=HTMLResponse)
def list_writeoff_acts(request: Request, db: Session = Depends(get_db)):
    items = crud_writeoff.get_writeoff_acts(db)
    return templates.TemplateResponse("writeoff_acts/list.html", {"request": request, "writeoff_acts": items})

@router.get("/create", response_class=HTMLResponse)
def create_writeoff_act_form(request: Request, db: Session = Depends(get_db)):
    orgs = crud_org.get_organizations(db)
    emps = crud_emp.get_employees(db)
    depts = crud_dept.get_departments(db)
    prods = crud_prod.get_products(db)
    return templates.TemplateResponse(
        "writeoff_acts/create.html",
        {"request": request, "orgs": orgs, "emps": emps, "depts": depts, "prods": prods}
    )

@router.post("/create")
def create_writeoff_act(
    request: Request,
    # Шапка документа
    organization_id: int = Form(...),
    act_number: str = Form(...),
    act_date: str = Form(...),
    commission_chairman_id: int = Form(...),
    commission_member1_id: int = Form(...),
    commission_member2_id: str = Form(None),
    commission_member3_id: str = Form(None),
    created_by_id: int = Form(...),
    department_id: int = Form(...),
    
    # Позиции
    product_id: List[str] = Form([]),
    inventory_number: List[str] = Form([]),
    commissioning_date: List[str] = Form([]),
    initial_cost: List[str] = Form([]),
    useful_life: List[str] = Form([]),
    actual_life: List[str] = Form([]),
    residual_value: List[str] = Form([]),
    item_reason: List[str] = Form([]),
    
    db: Session = Depends(get_db),
):
    # Обрабатываем необязательные поля комиссии
    commission_member2_id_int = None
    commission_member3_id_int = None
    
    if commission_member2_id and commission_member2_id.strip():
        try:
            commission_member2_id_int = int(commission_member2_id)
        except (ValueError, TypeError):
            commission_member2_id_int = None
    
    if commission_member3_id and commission_member3_id.strip():
        try:
            commission_member3_id_int = int(commission_member3_id)
        except (ValueError, TypeError):
            commission_member3_id_int = None

    # Собираем позиции акта
    items = []
    for i, (pid, inv_num) in enumerate(zip(product_id, inventory_number)):
        if not pid or not pid.strip() or not inv_num or not inv_num.strip():
            continue
            
        try:
            item = WriteOffActItemCreate(
                product_id=int(pid),
                inventory_number=inv_num,
                commissioning_date=commissioning_date[i] if i < len(commissioning_date) and commissioning_date[i] else None,
                initial_cost=float(initial_cost[i]) if i < len(initial_cost) and initial_cost[i] else 0.0,
                useful_life=int(useful_life[i]) if i < len(useful_life) and useful_life[i] else 0,
                actual_life=int(actual_life[i]) if i < len(actual_life) and actual_life[i] else 0,
                residual_value=float(residual_value[i]) if i < len(residual_value) and residual_value[i] else 0.0,
                item_reason=item_reason[i] if i < len(item_reason) and item_reason[i] else None,
            )
            items.append(item)
        except (ValueError, TypeError):
            continue

    obj_in = WriteOffActCreate(
        organization_id=organization_id,
        act_number=act_number,
        act_date=act_date,
        commission_chairman_id=commission_chairman_id,
        commission_member1_id=commission_member1_id,
        commission_member2_id=commission_member2_id_int,
        commission_member3_id=commission_member3_id_int,
        created_by_id=created_by_id,
        department_id=department_id,
        items=items,
    )
    crud_writeoff.create_writeoff_act(db, obj_in)
    return RedirectResponse(url="/writeoff-acts", status_code=303)

@router.get("/{act_id}", response_class=HTMLResponse)
def writeoff_act_detail(act_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud_writeoff.get_writeoff_act(db, act_id)
    if not item:
        raise HTTPException(status_code=404, detail="Акт списания не найден")
    return templates.TemplateResponse("writeoff_acts/detail.html", {"request": request, "act": item})

@router.get("/{act_id}/edit", response_class=HTMLResponse)
def edit_writeoff_act_form(act_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud_writeoff.get_writeoff_act(db, act_id)
    if not item:
        raise HTTPException(status_code=404, detail="Акт списания не найден")
    orgs = crud_org.get_organizations(db)
    emps = crud_emp.get_employees(db)
    depts = crud_dept.get_departments(db)
    prods = crud_prod.get_products(db)
    return templates.TemplateResponse(
        "writeoff_acts/edit.html",
        {"request": request, "act": item, "orgs": orgs, "emps": emps, "depts": depts, "prods": prods}
    )


@router.post("/{act_id}/edit")
def update_writeoff_act(
    act_id: int,
    request: Request,
    # Шапка документа
    organization_id: int = Form(...),
    act_number: str = Form(...),
    act_date: str = Form(...),
    commission_chairman_id: int = Form(...),
    commission_member1_id: int = Form(...),
    commission_member2_id: str = Form(None),
    commission_member3_id: str = Form(None),
    created_by_id: int = Form(...),
    department_id: int = Form(...),
    
    # Позиции
    product_id: List[str] = Form([]),
    inventory_number: List[str] = Form([]),
    commissioning_date: List[str] = Form([]),
    initial_cost: List[str] = Form([]),
    useful_life: List[str] = Form([]),
    actual_life: List[str] = Form([]),
    residual_value: List[str] = Form([]),
    item_reason: List[str] = Form([]),
    
    db: Session = Depends(get_db),
):
    # Обрабатываем необязательные поля комиссии
    commission_member2_id_int = None
    commission_member3_id_int = None
    
    if commission_member2_id and commission_member2_id.strip():
        try:
            commission_member2_id_int = int(commission_member2_id)
        except (ValueError, TypeError):
            commission_member2_id_int = None
    
    if commission_member3_id and commission_member3_id.strip():
        try:
            commission_member3_id_int = int(commission_member3_id)
        except (ValueError, TypeError):
            commission_member3_id_int = None

    # Собираем позиции акта
    items = []
    for i, (pid, inv_num) in enumerate(zip(product_id, inventory_number)):
        if not pid or not pid.strip() or not inv_num or not inv_num.strip():
            continue
            
        try:
            item = WriteOffActItemCreate(
                product_id=int(pid),
                inventory_number=inv_num,
                commissioning_date=commissioning_date[i] if i < len(commissioning_date) and commissioning_date[i] else None,
                initial_cost=float(initial_cost[i]) if i < len(initial_cost) and initial_cost[i] else 0.0,
                useful_life=int(useful_life[i]) if i < len(useful_life) and useful_life[i] else 0,
                actual_life=int(actual_life[i]) if i < len(actual_life) and actual_life[i] else 0,
                residual_value=float(residual_value[i]) if i < len(residual_value) and residual_value[i] else 0.0,
                item_reason=item_reason[i] if i < len(item_reason) and item_reason[i] else None,
            )
            items.append(item)
        except (ValueError, TypeError):
            continue

    obj_in = WriteOffActUpdate(
        organization_id=organization_id,
        act_number=act_number,
        act_date=act_date,
        commission_chairman_id=commission_chairman_id,
        commission_member1_id=commission_member1_id,
        commission_member2_id=commission_member2_id_int,
        commission_member3_id=commission_member3_id_int,
        created_by_id=created_by_id,
        department_id=department_id,
        items=items,
    )
    
    db_obj = crud_writeoff.get_writeoff_act(db, act_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Акт списания не найден")
    
    crud_writeoff.update_writeoff_act(db, db_obj, obj_in)
    return RedirectResponse(url="/writeoff-acts", status_code=303)
@router.get("/{act_id}/print", response_class=HTMLResponse)
def writeoff_act_print(act_id: int, request: Request, db: Session = Depends(get_db)):
    item = crud_writeoff.get_writeoff_act(db, act_id)
    if not item:
        raise HTTPException(status_code=404, detail="Акт списания не найден")
    return templates.TemplateResponse("writeoff_acts/print.html", {"request": request, "act": item})

@router.get("/{act_id}/delete", response_class=HTMLResponse)
def delete_writeoff_act_form(
    act_id: int, 
    request: Request, 
    db: Session = Depends(get_db)
):
    item = crud_writeoff.get_writeoff_act(db, act_id)
    if not item:
        raise HTTPException(status_code=404, detail="Акт списания не найден")
    return templates.TemplateResponse(
        "writeoff_acts/delete.html", 
        {"request": request, "act": item}
    )

@router.post("/{act_id}/delete")
def delete_writeoff_act(
    act_id: int, 
    db: Session = Depends(get_db)
):
    db_obj = crud_writeoff.get_writeoff_act(db, act_id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="Акт списания не найден")
    crud_writeoff.delete_writeoff_act(db, db_obj)
    return RedirectResponse(url="/writeoff-acts", status_code=303)