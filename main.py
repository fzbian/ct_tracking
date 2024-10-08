from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from api import containers, packages, health, status, config
from database import engine, Base

app = FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(containers.router, prefix="/containers", tags=["containers"])
app.include_router(packages.router, prefix="/packages", tags=["packages"])
app.include_router(health.router, prefix="/health", tags=["health"])
app.include_router(config.router, prefix="/config", tags=["config"])
app.include_router(status.router, prefix="/status", tags=["statuses"])

app.mount("/static", StaticFiles(directory="ui/staticfiles"), name="static")

@app.get("/")
def read_root():
    return {"Hello": "World"}
