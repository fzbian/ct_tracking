from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from api import utils
from models import Status, StatusCreate, StatusResponse, Package, StatusUpdateDate
from database import SessionLocal
import os
from dotenv import load_dotenv
load_dotenv()

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/{status_id}", response_model=StatusResponse)
def get_status(status_id: int, db: Session = Depends(get_db)):
    db_status = db.query(Status).filter(Status.id == status_id).first()
    
    if not db_status:
        raise HTTPException(status_code=404, detail="Status not found")

    return db_status

@router.post("/", response_model=StatusResponse)
def create_status(status: StatusCreate, db: Session = Depends(get_db)):
    package = db.query(Package).filter(Package.id == status.package_id).first()
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")

    db_status = Status(
        package_id=status.package_id,
        status=status.status,
        updated_at = status.updated_at
    )

    utils.send_message(1, package.tracking_id, package.contact_number, status.status)

    db.add(db_status)
    db.commit()
    db.refresh(db_status)

    return db_status

@router.put("/{status_id}/update-date", response_model=StatusResponse)
def update_status_date(status_id: int, updated_data: StatusUpdateDate, db: Session = Depends(get_db)):
    db_status = db.query(Status).filter(Status.id == status_id).first()
    
    if not db_status:
        raise HTTPException(status_code=404, detail="Status not found")

    # Actualizar la fecha
    db_status.updated_at = updated_data.updated_at

    db.commit()
    db.refresh(db_status)

    return db_status
