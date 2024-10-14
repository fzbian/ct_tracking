from typing import List
from fastapi import APIRouter
from api import utils
from models import Package, PackageCreate, PackageResponse, Container, PackageUpdate, StatusResponse, Status, \
    PackageWithContainerResponse, ContainerResponse
import random
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session
from database import SessionLocal
from io import *
import weasyprint


router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def generate_custom_id(db: Session) -> str:
    while True:
        random_numbers = random.randint(10000, 99999)  # Genera 5 dígitos aleatorios
        tracking_id = str(random_numbers)
        # Verificar si el tracking_id ya existe en la base de datos
        if not db.query(Package).filter(Package.tracking_id == tracking_id).first():
            return tracking_id

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

router = APIRouter()

@router.get("/downloadReceipt/{package_id}")
def download_receipt(package_id: int, db: Session = Depends(get_db)):
    db_package = db.query(Package).filter(Package.id == package_id).first()
    if not db_package:
        raise HTTPException(status_code=404, detail="Package not found")

    logo_path = "https://tracking.chinatownlogistic.com/static/logo.png"

    created_at = db_package.created_at.strftime("%d-%m-%Y")

    html_content = f"""
<!DOCTYPE html>
<html lang="">

<head>
	<title></title>
	<meta content="summary_large_image" name="twitter:card" />
	<meta content="website" property="og:type" />
	<meta content="" property="og:description" />
	<meta content="https://of567tzhns.preview-beefreedesign.com/ZCGjl" property="og:url" />
	<meta content="https://pro-bee-beepro-thumbnail.getbee.io/messages/1276261/1262412/2264210/11735807_large.jpg" property="og:image" />
	<meta content="" property="og:title" />
	<meta content="" name="description" />
	<meta charset="utf-8" />
	<meta content="width=device-width" name="viewport" />
	<style>
		.bee-row,
		.bee-row-content {{
			position: relative
		}}

		.bee-row-3,
		body {{
			background-color: #ffffff
		}}

		.bee-row-1,
		.bee-row-1 .bee-row-content,
		.bee-row-2,
		.bee-row-3 {{
			background-repeat: no-repeat
		}}

		body {{
			color: #000000;
			font-family: Arial, Helvetica, sans-serif
		}}

		a {{
			color: #7747FF
		}}

		* {{
			box-sizing: border-box
		}}

		body,
		h1 {{
			margin: 0
		}}

		.bee-row-content {{
			max-width: 1440px;
			margin: 0 auto;
			display: flex
		}}

		.bee-row-content .bee-col-w3 {{
			flex-basis: 25%
		}}

		.bee-row-content .bee-col-w9 {{
			flex-basis: 75%
		}}

		.bee-row-content .bee-col-w12 {{
			flex-basis: 100%
		}}

		.bee-icon .bee-icon-label-right a {{
			text-decoration: none
		}}

		.bee-divider,
		.bee-image {{
			overflow: auto
		}}

		.bee-divider .center,
		.bee-image .bee-center {{
			margin: 0 auto
		}}

		.bee-row-1 .bee-col-1 .bee-block-1 {{
			width: 100%
		}}

		.bee-icon {{
			display: inline-block;
			vertical-align: middle
		}}

		.bee-icon .bee-content {{
			display: flex;
			align-items: center
		}}

		.bee-image img {{
			display: block;
			width: 100%
		}}

		.bee-table table {{
			border-collapse: collapse;
			width: 100%
		}}

		.bee-table table tbody,
		.bee-table table thead {{
			vertical-align: top
		}}

		.bee-table table td,
		.bee-table table th {{
			padding: 10px;
			word-break: break-word
		}}

		@media (max-width:768px) {{
			.bee-row-content:not(.no_stack) {{
				display: block
			}}
		}}

		.bee-row-1 .bee-row-content {{
			border-radius: 0;
			color: #000000
		}}

		.bee-row-1 .bee-col-1,
		.bee-row-1 .bee-col-2,
		.bee-row-2 .bee-col-1,
		.bee-row-3 .bee-col-1 {{
			padding-bottom: 5px;
			padding-top: 5px
		}}

		.bee-row-1 .bee-col-2 .bee-block-1 {{
			padding: 10px;
			text-align: center;
			width: 100%
		}}

		.bee-row-2 .bee-row-content,
		.bee-row-3 .bee-row-content {{
			background-repeat: no-repeat;
			color: #000000
		}}

		.bee-row-2 .bee-col-1 .bee-block-1,
		.bee-row-2 .bee-col-1 .bee-block-2,
		.bee-row-2 .bee-col-1 .bee-block-3 {{
			padding: 10px
		}}

		.bee-row-3 .bee-col-1 .bee-block-1 {{
			color: #1e0e4b;
			font-family: Inter, sans-serif;
			font-size: 15px;
			padding-bottom: 5px;
			padding-top: 5px;
			text-align: center
		}}

		.bee-row-3 .bee-col-1 .bee-block-1 .bee-icon-image {{
			padding: 5px 6px 5px 5px
		}}

		.bee-row-3 .bee-col-1 .bee-block-1 .bee-icon:not(.bee-icon-first) .bee-content {{
			margin-left: 0
		}}

		.bee-row-3 .bee-col-1 .bee-block-1 .bee-icon::not(.bee-icon-last) .bee-content {{
			margin-right: 0
		}}
	</style>
</head>

<body>
	<div class="bee-page-container">
		<div class="bee-row bee-row-1">
			<div class="bee-row-content">
				<div class="bee-col bee-col-1 bee-col-w3">
					<div class="bee-block bee-block-1 bee-image"><img alt="" class="bee-center bee-fixedwidth" src="http://imgfz.com/i/4QA6BNT.png" style="max-width:108px;" /></div>
				</div>
				<div class="bee-col bee-col-2 bee-col-w9">
					<div class="bee-block bee-block-1 bee-heading">
						<h1 style="color:#000000;direction:ltr;font-family:Arial, Helvetica, sans-serif;font-size:18px;font-weight:700;letter-spacing:normal;line-height:150%;text-align:center;margin-top:0;margin-bottom:0;"><span class="tinyMce-placeholder">RECEIPT #{db_package.tracking_id}</span> </h1>
					</div>
				</div>
			</div>
		</div>
		<div class="bee-row bee-row-2">
			<div class="bee-row-content">
				<div class="bee-col bee-col-1 bee-col-w12">
					<div class="bee-block bee-block-1 bee-table">
						<table style="table-layout:fixed;direction:ltr;background-color:transparent;font-family:Arial, Helvetica, sans-serif;font-weight:400;color:#101112;text-align:left;letter-spacing:0px;">
							<thead style="background-color:#f2f2f2;color:#101112;font-size:14px;line-height:120%;text-align:left;">
								<tr>
									<th style="font-weight:700;border-top:1px solid #dddddd;border-right:1px solid #dddddd;border-bottom:1px solid #dddddd;border-left:1px solid #dddddd;">NAME</th>
									<th style="font-weight:700;border-top:1px solid #dddddd;border-right:1px solid #dddddd;border-bottom:1px solid #dddddd;border-left:1px solid #dddddd;">DATE</th>
								</tr>
							</thead>
							<tbody style="font-size:16px;line-height:120%;">
								<tr>
									<td style="border-top:1px solid #dddddd;border-right:1px solid #dddddd;border-bottom:1px solid #dddddd;border-left:1px solid #dddddd;">{db_package.pseudoname}</td>
									<td style="border-top:1px solid #dddddd;border-right:1px solid #dddddd;border-bottom:1px solid #dddddd;border-left:1px solid #dddddd;">{created_at}</td>
								</tr>
							</tbody>
						</table>
					</div>
					<div class="bee-block bee-block-2 bee-divider">
						<div class="center bee-separator" style="border-top:1px solid #dddddd;width:100%;"></div>
					</div>
					<div class="bee-block bee-block-3 bee-table">
						<table style="table-layout:fixed;direction:ltr;background-color:transparent;font-family:Arial, Helvetica, sans-serif;font-weight:400;color:#101112;text-align:left;letter-spacing:0px;">
							<thead style="background-color:#f2f2f2;color:#101112;font-size:14px;line-height:120%;text-align:center;">
								<tr>
									<th style="font-weight:700;border-top:1px solid #dddddd;border-right:1px solid #dddddd;border-bottom:1px solid #dddddd;border-left:1px solid #dddddd;">PACKING</th>
									<th style="font-weight:700;border-top:1px solid #dddddd;border-right:1px solid #dddddd;border-bottom:1px solid #dddddd;border-left:1px solid #dddddd;">PIECES</th>
									<th style="font-weight:700;border-top:1px solid #dddddd;border-right:1px solid #dddddd;border-bottom:1px solid #dddddd;border-left:1px solid #dddddd;">CBM</th>
									<th style="font-weight:700;border-top:1px solid #dddddd;border-right:1px solid #dddddd;border-bottom:1px solid #dddddd;border-left:1px solid #dddddd;">KG</th>
								</tr>
							</thead>
							<tbody style="font-size:14px;line-height:120%;">
								<tr>
									<td style="border-top:1px solid #dddddd;border-right:1px solid #dddddd;border-bottom:1px solid #dddddd;border-left:1px solid #dddddd;">{db_package.package_type}</td>
									<td style="border-top:1px solid #dddddd;border-right:1px solid #dddddd;border-bottom:1px solid #dddddd;border-left:1px solid #dddddd;">{db_package.pieces}</td>
									<td style="border-top:1px solid #dddddd;border-right:1px solid #dddddd;border-bottom:1px solid #dddddd;border-left:1px solid #dddddd;">{db_package.volumetric_measure}</td>
									<td style="border-top:1px solid #dddddd;border-right:1px solid #dddddd;border-bottom:1px solid #dddddd;border-left:1px solid #dddddd;">{db_package.weight}</td>
								</tr>
							</tbody>
						</table>
					</div>
				</div>
			</div>
		</div>
	</div>
</body>

</html>
    """

    pdf_file = BytesIO()
    weasyprint.HTML(string=html_content).write_pdf(pdf_file)

    return StreamingResponse(BytesIO(pdf_file.getvalue()), media_type='application/pdf',
                                headers={"Content-Disposition": f"attachment; filename={db_package.tracking_id}.pdf"})

@router.get("/downloadLabeled/{package_id}")
def download_package_info(package_id: int, db: Session = Depends(get_db)):
    db_package = db.query(Package).filter(Package.id == package_id).first()
    if not db_package:
        raise HTTPException(status_code=200, detail="Package not found")

    logo_path = "https://tracking.chinatownlogistic.com/static/logo_labeled.png"
    created_at = db_package.created_at.strftime("%d-%m-%Y")

    html_content = f"""
<!DOCTYPE html>
<html lang="">

<head>
	<title></title>
	<meta content="summary_large_image" name="twitter:card" />
	<meta content="website" property="og:type" />
	<meta content="" property="og:description" />
	<meta content="https://of567tzhns.preview-beefreedesign.com/ZCGjl" property="og:url" />
	<meta content="https://pro-bee-beepro-thumbnail.getbee.io/messages/1276261/1262412/2264210/11735807_large.jpg" property="og:image" />
	<meta content="" property="og:title" />
	<meta content="" name="description" />
	<meta charset="utf-8" />
	<meta content="width=device-width" name="viewport" />
	<style>
		.bee-row,
		.bee-row-content {{
			position: relative
		}}

		.bee-row-5,
		body {{
			background-color: #ffffff
		}}

		.bee-row-1,
		.bee-row-2,
		.bee-row-3,
		.bee-row-4,
		.bee-row-5,
		.bee-row-5 .bee-row-content {{
			background-repeat: no-repeat
		}}

		body {{
			color: #000000;
			font-family: Arial, Helvetica, sans-serif
		}}

		a {{
			color: #7747FF
		}}

		* {{
			box-sizing: border-box
		}}

		body,
		h1 {{
			margin: 0
		}}

		.bee-row-content {{
			max-width: 1440px;
			margin: 0 auto;
			display: flex
		}}

		.bee-row-content .bee-col-w12 {{
			flex-basis: 100%
		}}

		.bee-icon .bee-icon-label-right a {{
			text-decoration: none
		}}

		.bee-image {{
			overflow: auto
		}}

		.bee-image .bee-center {{
			margin: 0 auto
		}}

		.bee-row-1 .bee-col-1 .bee-block-1 {{
			width: 100%
		}}

		.bee-row-1 .bee-col-1,
		.bee-row-2 .bee-col-1,
		.bee-row-3 .bee-col-1,
		.bee-row-4 .bee-col-1,
		.bee-row-5 .bee-col-1,
		.bee-row-5 .bee-col-1 .bee-block-1 {{
			padding-bottom: 5px;
			padding-top: 5px
		}}

		.bee-icon {{
			display: inline-block;
			vertical-align: middle
		}}

		.bee-icon .bee-content {{
			display: flex;
			align-items: center
		}}

		.bee-image img {{
			display: block;
			width: 100%
		}}

		@media (max-width:768px) {{
			.bee-row-content:not(.no_stack) {{
				display: block
			}}
		}}

		.bee-row-1 .bee-row-content,
		.bee-row-2 .bee-row-content,
		.bee-row-3 .bee-row-content,
		.bee-row-4 .bee-row-content {{
			background-repeat: no-repeat;
			border-radius: 0;
			color: #000000
		}}

		.bee-row-2 .bee-col-1 .bee-block-1,
		.bee-row-3 .bee-col-1 .bee-block-1,
		.bee-row-3 .bee-col-1 .bee-block-2,
		.bee-row-3 .bee-col-1 .bee-block-3 {{
			text-align: center;
			width: 100%
		}}

		.bee-row-5 .bee-row-content {{
			color: #000000
		}}

		.bee-row-5 .bee-col-1 .bee-block-1 {{
			color: #1e0e4b;
			font-family: Inter, sans-serif;
			font-size: 15px;
			text-align: center
		}}

		.bee-row-5 .bee-col-1 .bee-block-1 .bee-icon-image {{
			padding: 5px 6px 5px 5px
		}}

		.bee-row-5 .bee-col-1 .bee-block-1 .bee-icon:not(.bee-icon-first) .bee-content {{
			margin-left: 0
		}}

		.bee-row-5 .bee-col-1 .bee-block-1 .bee-icon::not(.bee-icon-last) .bee-content {{
			margin-right: 0
		}}
	</style>
</head>

<body>
	<div class="bee-page-container">
		<div class="bee-row bee-row-1">
			<div class="bee-row-content">
				<div class="bee-col bee-col-1 bee-col-w12">
					<div class="bee-block bee-block-1 bee-image"><img alt="" class="bee-center bee-fixedwidth" src="http://imgfz.com/i/gCbQAPJ.png" style="max-width:216px;" /></div>
				</div>
			</div>
		</div>
		<div class="bee-row bee-row-2">
			<div class="bee-row-content">
				<div class="bee-col bee-col-1 bee-col-w12">
					<div class="bee-block bee-block-1 bee-heading">
						<h1 style="color:#000000;direction:ltr;font-family:'Helvetica Neue', Helvetica, Arial, sans-serif;font-size:90px;font-weight:700;letter-spacing:normal;line-height:150%;text-align:center;margin-top:0;margin-bottom:0;"><span class="tinyMce-placeholder">{db_package.tracking_id}</span> </h1>
					</div>
				</div>
			</div>
		</div>
		<div class="bee-row bee-row-3">
			<div class="bee-row-content">
				<div class="bee-col bee-col-1 bee-col-w12">
					<div class="bee-block bee-block-1 bee-heading">
						<h1 style="color:#000000;direction:ltr;font-family:Arial, Helvetica, sans-serif;font-size:56px;font-weight:700;letter-spacing:1px;line-height:150%;text-align:center;margin-top:0;margin-bottom:0;"><span class="tinyMce-placeholder">{db_package.pseudoname}</span> </h1>
					</div>
					<div class="bee-block bee-block-2 bee-heading">
						<h1 style="color:#000000;direction:ltr;font-family:Arial, Helvetica, sans-serif;font-size:56px;font-weight:700;letter-spacing:1px;line-height:150%;text-align:center;margin-top:0;margin-bottom:0;"><span class="tinyMce-placeholder">{created_at}</span> </h1>
					</div>
					<div class="bee-block bee-block-3 bee-heading">
						<h1 style="color:#000000;direction:ltr;font-family:Arial, Helvetica, sans-serif;font-size:56px;font-weight:700;letter-spacing:1px;line-height:150%;text-align:center;margin-top:0;margin-bottom:0;"><span class="tinyMce-placeholder">PCS {db_package.pieces}</span> </h1>
					</div>
				</div>
			</div>
		</div>
		<div class="bee-row bee-row-4">
			<div class="bee-row-content">
				<div class="bee-col bee-col-1 bee-col-w12"></div>
			</div>
		</div>
	</div>
</body>

</html>
    """

    pdf_file = BytesIO()
    weasyprint.HTML(string=html_content).write_pdf(pdf_file)

    return StreamingResponse(BytesIO(pdf_file.getvalue()), media_type='application/pdf',
                             headers={"Content-Disposition": f"attachment; filename=labeled-{db_package.tracking_id}.pdf"})

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
    tracking_id = generate_custom_id(db)

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
        delivered=False,
        created_at = package.created_at
    )
    db.add(db_package)
    db.commit()
    db.refresh(db_package)
    utils.send_message(0, tracking_id, package.contact_number, "")

    status = Status(package_id=db_package.id, status="RECIBIMOS TU ENVIO")
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
        delivered=db_package.delivered,  # Aquí se añade el campo delivered
        created_at=db_package.created_at  # Añadido created_at
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
    if package.created_at is not None:
        db_package.created_at = package.created_at

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

