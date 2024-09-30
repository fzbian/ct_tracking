from typing import List

from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from models import Package, PackageCreate, PackageResponse, Container, PackageUpdate, StatusResponse, Status, \
    PackageWithContainerResponse, ContainerResponse
from database import SessionLocal
import random

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_custom_id(pseudoname: str) -> str:
    random_numbers = random.randint(1000, 9999)  # Genera 4 dígitos aleatorios
    pseudoname_part = pseudoname[:4].upper()  # Toma las primeras 4 letras del pseudoname
    return f"PAQ{random_numbers}{pseudoname_part}"


from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from models import Package
from database import SessionLocal
from weasyprint import HTML
import io

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/download/{package_id}")
def download_package_info(package_id: int, db: Session = Depends(get_db)):
    # Buscar el paquete por ID
    db_package = db.query(Package).filter(Package.id == package_id).first()
    if not db_package:
        raise HTTPException(status_code=404, detail="Package not found")

    # Obtener todos los estados asociados al paquete
    statuses = db_package.statuses

    # Generar el HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Package Info - {db_package.tracking_id}</title>
        <style>
            body {{
                background-color: #f8f9fa;
                font-family: Arial, sans-serif;
            }}
            .header-title {{
                color: #dc3545;
                font-weight: bold;
                text-align: center;
                margin-top: 20px;
            }}
            .container {{
                margin: 20px;
                padding: 20px;
                background-color: #fff;
                border-radius: 8px;
                box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
            }}
            .logo {{
                height: 40px;
                margin-right: 10px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1 class="header-title">Package Information</h1>
            <p><strong>Tracking ID:</strong> {db_package.tracking_id}</p>
            <p><strong>Pseudoname:</strong> {db_package.pseudoname}</p>
            <p><strong>Weight:</strong> {db_package.weight} kg</p>
            <p><strong>Volumetric Measure:</strong> {db_package.volumetric_measure} m³</p>
            <p><strong>Contact Number:</strong> {db_package.contact_number}</p>
    """

    html_content += """
            </ul>
        </div>
    </body>
    </html>
    """

    # Convertir HTML a PDF
    pdf_file = HTML(string=html_content).write_pdf()

    # Retornar el PDF como respuesta
    return StreamingResponse(io.BytesIO(pdf_file), media_type='application/pdf', headers={"Content-Disposition": f"attachment; filename=package_info_{package_id}.pdf"})

@router.put("/{package_id}/deliver", response_model=PackageResponse)
def deliver_package(package_id: int, db: Session = Depends(get_db)):
    # Buscar el paquete por ID
    db_package = db.query(Package).filter(Package.id == package_id).first()
    if not db_package:
        raise HTTPException(status_code=404, detail="Package not found")

    # Marcar el paquete como entregado
    db_package.delivered = True

    # Commit de los cambios en la base de datos
    db.commit()
    db.refresh(db_package)

    return db_package

# deliver package for all packages in a container
@router.put("/deliverByContainer/{container_id}", response_model=List[PackageResponse])
def deliver_package_by_container(container_id: int, db: Session = Depends(get_db)):
    # Buscar el contenedor por ID
    container = db.query(Container).filter(Container.id == container_id).first()
    if not container:
        raise HTTPException(status_code=404, detail="Container not found")

    # Marcar todos los paquetes del contenedor como entregados
    db.query(Package).filter(Package.container_id == container_id).update({Package.delivered: True}, synchronize_session=False)
    db.commit()

    # Obtener los paquetes actualizados
    packages = db.query(Package).filter(Package.container_id == container_id).all()
    return packages

@router.post("/", response_model=PackageResponse)
def create_package(package: PackageCreate, db: Session = Depends(get_db)):
    container = db.query(Container).filter(Container.id == package.container_id).first()
    if not container:
        raise HTTPException(status_code=404, detail="Container not found")

    # Generar tracking ID personalizado
    tracking_id = generate_custom_id(package.pseudoname)

    # Crear el paquete con el tracking ID y el nuevo campo package_type
    db_package = Package(
        pseudoname=package.pseudoname,
        weight=package.weight,
        volumetric_measure=package.volumetric_measure,
        pieces=package.pieces,
        contact_number=package.contact_number,
        container_id=package.container_id,
        tracking_id=tracking_id,  # Nuevo tracking ID
        package_type=package.package_type,  # Nuevo atributo package_type
        delivered=False  # Nuevo atributo delivered
    )
    db.add(db_package)
    db.commit()
    db.refresh(db_package)

    # Agregar un nuevo estado a ese paquete "EN PREPARACION"
    status = Status(package_id=db_package.id, status="EN PREPARACION")
    db.add(status)
    db.commit()

    return db_package

@router.get("/getInfoByTrackingId/{tracking_id}", response_model=PackageWithContainerResponse)
def get_info_by_tracking_id(tracking_id: str, db: Session = Depends(get_db)):
    db_package = db.query(Package).filter(Package.tracking_id == tracking_id).first()
    if not db_package:
        raise HTTPException(status_code=404, detail="Package not found")

    statuses = db_package.statuses
    container = db_package.container

    # Incluir los nuevos atributos en la respuesta
    package_response = PackageWithContainerResponse(
        id=db_package.id,
        tracking_id=db_package.tracking_id,
        pseudoname=db_package.pseudoname,
        weight=db_package.weight,
        volumetric_measure=db_package.volumetric_measure,
        pieces=db_package.pieces,
        contact_number=db_package.contact_number,
        package_type=db_package.package_type,  # Añadido package_type
        container_id=db_package.container_id,
        container=ContainerResponse.from_orm(container) if container else None,
        statuses=[StatusResponse.from_orm(status) for status in statuses],
        delivered=db_package.delivered  # Aquí se añade el campo delivered
    )

    return package_response

@router.get("/", response_model=List[PackageResponse])
def get_packages(db: Session = Depends(get_db)):
    packages = db.query(Package).all()
    return packages

@router.put("/{package_id}", response_model=PackageResponse)
def update_package(package_id: int, package: PackageUpdate, db: Session = Depends(get_db)):
    # Buscar el paquete por ID
    db_package = db.query(Package).filter(Package.id == package_id).first()
    if not db_package:
        raise HTTPException(status_code=404, detail="Package not found")

    # Actualizar solo los campos proporcionados
    if package.pseudoname is not None:
        db_package.pseudoname = package.pseudoname
    if package.weight is not None:
        db_package.weight = package.weight
    if package.volumetric_measure is not None:
        db_package.volumetric_measure = package.volumetric_measure
    if package.pieces is not None:
        db_package.pieces = package.pieces
    if package.contact_number is not None:
        db_package.contact_number = package.contact_number
    if package.delivered is not None:
        db_package.delivered = package.delivered
    if package.package_type is not None:
        db_package.package_type = package.package_type

    # Commit de los cambios en la base de datos
    db.commit()
    db.refresh(db_package)

    return db_package

@router.get("/{package_id}", response_model=PackageResponse)
def get_package(package_id: int, db: Session = Depends(get_db)):
    db_package = db.query(Package).filter(Package.id == package_id).first()
    if not db_package:
        raise HTTPException(status_code=404, detail="Package not found")
    return db_package

# get all status by package
@router.get("/getStatusByPackage/{package_id}")
def get_status_by_package(package_id: int, db: Session = Depends(get_db)):
    db_package = db.query(Package).filter(Package.id == package_id).first()
    if not db_package:
        raise HTTPException(status_code=404, detail="Package not found")

    # Obtener todos los estados asociados al paquete
    statuses = db_package.statuses  # Usa la relación definida en el modelo
    return {"package_id": package_id, "statuses": [StatusResponse.from_orm(status) for status in statuses]}

# delete all statuses of the package and delete the package
@router.delete("/{package_id}")
def delete_package(package_id: int, db: Session = Depends(get_db)):
    db_package = db.query(Package).filter(Package.id == package_id).first()
    if not db_package:
        raise HTTPException(status_code=404, detail="Package not found")

    # Eliminar todos los estados asociados al paquete
    db.query(Status).filter(Status.package_id == package_id).delete()

    # Eliminar el paquete
    db.delete(db_package)
    db.commit()
    return {"message": "Package deleted"}

