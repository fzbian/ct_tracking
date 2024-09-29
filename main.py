from fastapi import FastAPI
from api import containers, packages, health, status, config
from database import engine, Base

app = FastAPI()

# Create the tables in the database
Base.metadata.create_all(bind=engine)

# Include the routers
app.include_router(containers.router, prefix="/containers", tags=["containers"])
app.include_router(packages.router, prefix="/packages", tags=["packages"])
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(config.router, prefix="/config", tags=["config"])
app.include_router(status.router, prefix="/status", tags=["statuses"])


@app.get("/")
def read_root():
    return {"Hello": "World"}
