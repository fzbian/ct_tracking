from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Status, StatusCreate, StatusResponse, Package
from database import SessionLocal
from twilio.rest import Client
import os
# env
from dotenv import load_dotenv
load_dotenv()

"""account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)"""

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=StatusResponse)
def create_status(status: StatusCreate, db: Session = Depends(get_db)):
    package = db.query(Package).filter(Package.id == status.package_id).first()
    if not package:
        raise HTTPException(status_code=404, detail="Package not found")

    db_status = Status(
        package_id=status.package_id,
        status=status.status
    )

    """message = client.messages.create(
        from_='whatsapp:+14155238886',
        body=f"ChinaTown Tracking le informa que su paquete {package.tracking_id} se encuentra en estado {status.status}, puedes revisar todos los estados de tu paquete ingresando a {os.getenv('PROTOCOL')}://{os.getenv('UI_SERVER')}:{os.getenv('UI_PORT')}/track/{package.tracking_id}",
        to=f"whatsapp:+57{package.contact_number}",
    )"""

    db.add(db_status)
    db.commit()
    db.refresh(db_status)

    return db_status
