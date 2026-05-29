from sqlalchemy.orm import Session
from .. import models
from ..schemas import writeoff_acts as schemas

def create_writeoff_act(db: Session, obj_in: schemas.WriteOffActCreate):
    db_obj = models.WriteOffAct(
        organization_id=obj_in.organization_id,
        act_number=obj_in.act_number,
        act_date=obj_in.act_date,
        commission_chairman_id=obj_in.commission_chairman_id,
        commission_member1_id=obj_in.commission_member1_id,
        commission_member2_id=obj_in.commission_member2_id,
        commission_member3_id=obj_in.commission_member3_id,
        created_by_id=obj_in.created_by_id,
        department_id=obj_in.department_id,
    )
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    
    for item_in in obj_in.items:
        item_db = models.WriteOffActItem(
            writeoff_act_id=db_obj.id,
            product_id=item_in.product_id,
            inventory_number=item_in.inventory_number,
            commissioning_date=item_in.commissioning_date,
            initial_cost=item_in.initial_cost,
            useful_life=item_in.useful_life,
            actual_life=item_in.actual_life,
            residual_value=item_in.residual_value,
            item_reason=item_in.item_reason,
        )
        db.add(item_db)
    
    db.commit()
    db.refresh(db_obj)
    return db_obj

def get_writeoff_act(db: Session, act_id: int):
    return db.query(models.WriteOffAct).filter(models.WriteOffAct.id == act_id).first()

def get_writeoff_acts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.WriteOffAct).offset(skip).limit(limit).all()

def update_writeoff_act(db: Session, db_obj: models.WriteOffAct, obj_in: schemas.WriteOffActUpdate):
    # Обновляем основные поля
    db_obj.organization_id = obj_in.organization_id
    db_obj.act_number = obj_in.act_number
    db_obj.act_date = obj_in.act_date
    db_obj.commission_chairman_id = obj_in.commission_chairman_id
    db_obj.commission_member1_id = obj_in.commission_member1_id
    db_obj.commission_member2_id = obj_in.commission_member2_id
    db_obj.commission_member3_id = obj_in.commission_member3_id
    db_obj.created_by_id = obj_in.created_by_id
    db_obj.department_id = obj_in.department_id
    db.query(models.WriteOffActItem).filter(
        models.WriteOffActItem.writeoff_act_id == db_obj.id
    ).delete()
    
    for item_in in obj_in.items:
        item_db = models.WriteOffActItem(
            writeoff_act_id=db_obj.id,
            product_id=item_in.product_id,
            inventory_number=item_in.inventory_number,
            commissioning_date=item_in.commissioning_date,
            initial_cost=item_in.initial_cost,
            useful_life=item_in.useful_life,
            actual_life=item_in.actual_life,
            residual_value=item_in.residual_value,
            item_reason=item_in.item_reason,
        )
        db.add(item_db)
    
    db.commit()
    db.refresh(db_obj)
    return db_obj

def delete_writeoff_act(db: Session, db_obj: models.WriteOffAct):
    db.delete(db_obj)
    db.commit()
    return True