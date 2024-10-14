from typing import List

from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks
from sqlalchemy.exc import SQLAlchemyError, IntegrityError
from sqlalchemy.orm import Session
from api import utils
from models import Container, ContainerCreate, ContainerResponse, PackageResponse, StatusCreate, Status, StatusUpdate, \
    Package
from database import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/", response_model=ContainerResponse)
def create_container(container: ContainerCreate, db: Session = Depends(get_db)):
    db_container = Container(
        identifier_name=container.identifier_name,
        shipment_type=container.shipment_type
    )
    db.add(db_container)
    db.commit()
    db.refresh(db_container)
    return db_container

@router.get("/", response_model=List[ContainerResponse])
def get_containers(db: Session = Depends(get_db)):
    containers = db.query(Container).all()
    return containers


@router.post("/archive/{container_id}")
def archive_container(container_id: int, db: Session = Depends(get_db)):
    container = db.query(Container).filter(
        Container.id == container_id).first()
    if not container:
        raise HTTPException(status_code=404, detail="Container not found")

    # Cambiar el estado de archivado
    # Cambia el estado (archivar/desarchivar)
    container.active = not container.active
    db.commit()

    return {
        "container_id": container_id,
        "archived": container.active,
        "message": "Container archived" if container.active else "Container unarchived"
    }


@router.get("/getContainerById/{container_id}", response_model=ContainerResponse)
def get_container_by_id(container_id: int, db: Session = Depends(get_db)):
    db_container = db.query(Container).filter(
        Container.id == container_id).first()

    if db_container is None:
        raise HTTPException(status_code=404, detail="Container not found")

    return db_container


@router.get("/getPackagesByContainer/{container_id}", response_model=List[PackageResponse])
def get_packages_by_container(container_id: int, db: Session = Depends(get_db)):
    # Verificar si el contenedor existe
    container = db.query(Container).filter(
        Container.id == container_id).first()
    if not container:
        raise HTTPException(status_code=404, detail="Container not found")

    packages = container.packages
    if not packages:
        raise HTTPException(
            status_code=200, detail="No packages found for this container")

    return packages


@router.get("/getValuesByContainer/{container_id}")
def get_values_by_container(container_id: int, db: Session = Depends(get_db)):
    # Verificar si el contenedor existe
    container = db.query(Container).filter(
        Container.id == container_id).first()
    if not container:
        raise HTTPException(status_code=404, detail="Container not found")

    # Obtener los paquetes del contenedor
    packages = container.packages
    if not packages:
        raise HTTPException(
            status_code=200, detail="No packages found for this container")

    # Calcular el total del peso y de la medida volumétrica
    total_weight = sum(package.weight for package in packages)
    total_volumetric_measure = sum(
        package.volumetric_measure for package in packages)

    return {
        "container_id": container_id,
        "total_weight": total_weight,
        "total_volumetric_measure": total_volumetric_measure
    }

@router.post("/changeStatusByContainer/{container_id}")
def change_status_by_container(
    container_id: int,
    status_data: StatusUpdate,
    background_tasks: BackgroundTasks,  # Mover esto antes del argumento con valor por defecto
    db: Session = Depends(get_db)
):
    # Verificar si el contenedor existe
    container = db.query(Container).filter(Container.id == container_id).first()
    if not container:
        raise HTTPException(status_code=404, detail="Container not found")

    # Obtener todos los paquetes del contenedor
    packages = container.packages
    if not packages:
        raise HTTPException(status_code=404, detail="No packages found for this container")

    # Cambiar el estado de cada paquete
    for package in packages:
        db_status = Status(
            package_id=package.id,
            status=status_data.status  # El estado es proporcionado en el JSON
        )
        db.add(db_status)

        # Añadir el envío de mensajes a las tareas en segundo plano
        background_tasks.add_task(utils.send_message, 1, package.tracking_id, package.contact_number, status_data.status)

    db.commit()

    return {
        "container_id": container_id,
        "status": status_data.status,
        "message": f"Status updated for {len(packages)} packages"
    }

@router.get("/getContainerStatuses/{container_id}")
def get_container_statuses(container_id: int, db: Session = Depends(get_db)):
    # Verificar si el contenedor existe
    container = db.query(Container).filter(
        Container.id == container_id).first()
    if not container:
        raise HTTPException(status_code=404, detail="Container not found")

    # Obtener todos los paquetes del contenedor
    packages = container.packages
    if not packages:
        raise HTTPException(
            status_code=404, detail="No packages found for this container")

    # Obtener todos los estados de los paquetes y consolidarlos
    statuses = []
    for package in packages:
        package_statuses = db.query(Status).filter(
            Status.package_id == package.id).all()
        for status in package_statuses:
            statuses.append({
                "status": status.status,
                "updated_at": status.updated_at
            })

    if not statuses:
        raise HTTPException(
            status_code=404, detail="No statuses found for this container")

    # Ordenar los estados por la fecha de actualización
    statuses.sort(key=lambda x: x["updated_at"])

    # Eliminar duplicados por 'status' para evitar repetidos
    unique_statuses = []
    seen = set()
    for status in statuses:
        if status["status"] not in seen:
            unique_statuses.append(status)
            seen.add(status["status"])

    return {
        "container_id": container_id,
        "statuses": unique_statuses
    }


@router.delete("/{container_id}")
def delete_container(container_id: int, db: Session = Depends(get_db)):
    try:
        # Step 1: Delete statuses associated with the packages in the container
        packages = db.query(Package).filter(
            Package.container_id == container_id).all()
        for package in packages:
            db.query(Status).filter(Status.package_id ==
                                    package.id).delete(synchronize_session=False)

        # Step 2: Delete the packages in the container
        db.query(Package).filter(Package.container_id ==
                                 container_id).delete(synchronize_session=False)

        # Step 3: Delete the container
        result = db.query(Container).filter(
            Container.id == container_id).delete(synchronize_session=False)
        if result == 0:
            raise HTTPException(status_code=404, detail="Container not found")

        db.commit()
        return {"detail": "Container and associated packages and statuses deleted successfully"}

    except IntegrityError:
        db.rollback()
        raise HTTPException(
            status_code=400, detail="Integrity error occurred during deletion")

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=str(e))
