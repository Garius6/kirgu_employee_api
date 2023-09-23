import uvicorn
from fastapi import Depends, FastAPI

from .database import models
from .database.databese import engine
from .repositories.main_repository import MainRepository, Repository
from .schemas import User, UserCreate, WTAEvent, WTAEventCreate
from .settings import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.application_name)


@app.post("/users/")
def create_user(
    user: UserCreate,
    repository: Repository = Depends(MainRepository),
) -> int:
    return repository.create_user(user)


@app.get("/users/")
def get_users(
    repository: Repository = Depends(MainRepository),
) -> list[User]:
    return repository.get_users()


@app.post("/events/")
def create_event(
    event: WTAEventCreate,
    repository: Repository = Depends(MainRepository),
) -> int:
    return repository.create_wta_event(event)


@app.get("/events/")
def get_events(
    repository: MainRepository = Depends(MainRepository),
) -> list[WTAEvent]:
    return repository.get_wta_events()


@app.get("/healthcheck")
def healthcheck():
    return "ok"


if __name__ == "__main__":
    uvicorn.run(  # noqa: F821
        "kirgu_employee.main:app",
        host=settings.host,
        port=settings.port,
        reload=True,
    )
