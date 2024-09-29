from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import SessionLocal

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/reset-database")
def reset_database(db: Session = Depends(get_db)):
    try:
        # Desactivar restricciones de claves foráneas
        db.execute(text("SET FOREIGN_KEY_CHECKS = 0;"))

        # Intentar eliminar las claves foráneas (puedes manejar el error si no existen)
        try:
            db.execute(text("ALTER TABLE statuses DROP FOREIGN KEY fk_package_id;"))
        except Exception:
            pass  # Ignorar si no existe

        try:
            db.execute(text("ALTER TABLE packages DROP FOREIGN KEY fk_container_id;"))
        except Exception:
            pass  # Ignorar si no existe

        # Truncar las tablas y reiniciar AUTO_INCREMENT
        db.execute(text("TRUNCATE TABLE statuses;"))
        db.execute(text("TRUNCATE TABLE packages;"))
        db.execute(text("TRUNCATE TABLE containers;"))

        # Restaurar las claves foráneas
        db.execute(text(
            "ALTER TABLE packages ADD CONSTRAINT fk_container_id FOREIGN KEY (container_id) REFERENCES containers(id);"))
        db.execute(
            text("ALTER TABLE statuses ADD CONSTRAINT fk_package_id FOREIGN KEY (package_id) REFERENCES packages(id);"))

        # Reactivar restricciones de claves foráneas
        db.execute(text("SET FOREIGN_KEY_CHECKS = 1;"))

        # Confirmar la transacción
        db.commit()

        return {"message": "Database reset and constraints restored successfully"}

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"An error occurred: {str(e)}")
