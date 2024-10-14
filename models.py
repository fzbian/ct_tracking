from sqlalchemy import Column, Integer, String, Text, ForeignKey, Double, BigInteger, TIMESTAMP, func, Float, Boolean
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

Base = declarative_base()

class Container(Base):
    __tablename__ = 'containers'

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    identifier_name = Column(Text, nullable=False)
    shipment_type = Column(Text, nullable=False)
    active = Column(Boolean, default=True, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    packages = relationship("Package", back_populates="container")

    class Config:
        orm_mode = True

class Package(Base):
    __tablename__ = 'packages'

    id = Column(Integer, primary_key=True, index=True)
    tracking_id = Column(String(255), nullable=False, unique=True)
    pseudoname = Column(String, nullable=False)
    weight = Column(Float, nullable=False)
    volumetric_measure = Column(Float, nullable=False)
    contact_number = Column(BigInteger, nullable=False)
    pieces = Column(Integer, nullable=False)  # Atributo existente
    container_id = Column(Integer, ForeignKey('containers.id'), nullable=True)
    delivered = Column(Boolean, default=False)
    package_type = Column(Text, nullable=True)  # Atributo existente
    created_at = Column(TIMESTAMP, server_default=func.now())  # Nueva columna automatizada

    statuses = relationship("Status", back_populates="package", cascade="all, delete-orphan")
    container = relationship("Container", back_populates="packages")

    class Config:
        orm_mode = True

class Status(Base):
    __tablename__ = 'statuses'

    id = Column(BigInteger, primary_key=True, index=True)
    package_id = Column(Integer, ForeignKey('packages.id'), nullable=False)
    status = Column(String, nullable=False)
    updated_at = Column(TIMESTAMP, server_default=func.now(), onupdate=func.now())

    package = relationship("Package", back_populates="statuses")

    class Config:
        orm_mode = True
        from_attributes = True

# Modelos Pydantic
class ContainerCreate(BaseModel):
    identifier_name: str
    shipment_type: str
    active: Optional[bool] = True

    class Config:
        orm_mode = True

class ContainerResponse(BaseModel):
    id: int
    identifier_name: str
    shipment_type: str
    active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

class StatusResponse(BaseModel):
    id: int
    package_id: int
    status: str
    updated_at: datetime

    class Config:
        orm_mode = True
        from_attributes = True

class PackageWithContainerResponse(BaseModel):
    id: int
    tracking_id: str
    pseudoname: str
    weight: float
    volumetric_measure: float
    contact_number: int
    pieces: int  # Atributo existente
    container_id: Optional[int] = None
    package_type: Optional[str] = None  # Atributo existente
    created_at: datetime  # Nuevo atributo en la respuesta
    container: Optional[ContainerResponse] = None
    statuses: List[StatusResponse] = []
    delivered: bool

    class Config:
        orm_mode = True
        from_attributes = True

class PackageCreate(BaseModel):
    pseudoname: str
    weight: float
    volumetric_measure: float
    contact_number: int
    pieces: int  # Atributo existente
    container_id: Optional[int] = None
    package_type: Optional[str] = None  # Atributo existente
    created_at: datetime

class PackageResponse(BaseModel):
    id: int
    tracking_id: str
    pseudoname: str
    weight: float
    volumetric_measure: float
    contact_number: int
    pieces: int  # Atributo existente
    container_id: Optional[int] = None
    delivered: bool
    package_type: Optional[str]  # Atributo existente
    created_at: datetime  # Nuevo atributo en la respuesta

    class Config:
        orm_mode = True
        from_attributes = True

class StatusCreate(BaseModel):
    package_id: int
    status: str
    updated_at: Optional[datetime] = datetime.now()  # Si no se pasa valor, se asigna la hora actual

    class Config:
        orm_mode = True


class StatusUpdate(BaseModel):
    status: str

    class Config:
        orm_mode = True

class StatusUpdateDate(BaseModel):
    updated_at: datetime

    class Config:
        orm_mode = True

class PackageUpdate(BaseModel):
    pseudoname: Optional[str] = None
    weight: Optional[float] = None
    volumetric_measure: Optional[float] = None
    contact_number: Optional[int] = None
    pieces: Optional[int] = None  # Atributo existente
    delivered: Optional[bool] = None
    package_type: Optional[str] = None  # Atributo existente para actualizar
    created_at: Optional[datetime] = None  # Corrige la definición aquí

    class Config:
        orm_mode = True