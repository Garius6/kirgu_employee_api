from fastapi import Depends, FastAPI

from src.database import models
from src.repositories.main_repository import MainRepository

from .database.databese import engine
from .schemas import UserCreate, User, WTAEvent, WTAEventCreate
from .settings import settings

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title=settings.application_name)


@app.post("/users/")
def create_user(
    user: UserCreate,
    repository: MainRepository = Depends(MainRepository),
) -> int:
    return repository.create_user(user)


@app.get("/users/")
def get_users(
    repository: MainRepository = Depends(MainRepository),
) -> list[User]:
    return repository.get_users()


@app.post("/events/")
def create_event(
    event: WTAEventCreate,
    repository: MainRepository = Depends(MainRepository),
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
