from datetime import timedelta
from typing import Annotated
from fastapi.security import OAuth2PasswordRequestForm
import uvicorn
from fastapi import Depends, FastAPI, HTTPException, status

from kirgu_employee.dependencies import get_current_active_user
from kirgu_employee.repositories.main_repository import MainRepository, Repository
from kirgu_employee.schemas import Token, User, UserCreate, WTAEvent, WTAEventCreate
from kirgu_employee.settings import settings

app = FastAPI(title=settings.application_name)


@app.post("/users", status_code=status.HTTP_201_CREATED, response_model=int)
def create_user(
    user: UserCreate,
    repository: Annotated[Repository, Depends(MainRepository)],
    current_active_user: Annotated[User, Depends(get_current_active_user)],
):
    return repository.create_user(user)


@app.get("/users", response_model=list[User])
def get_users(
    repository: Annotated[Repository, Depends(MainRepository)],
    current_active_user: Annotated[User, Depends(get_current_active_user)],
):
    return repository.get_users()


@app.post(
    "/users/{user_id}/events/", status_code=status.HTTP_201_CREATED, response_model=int
)
def create_event(
    event: WTAEventCreate,
    user_id: int,
    repository: Annotated[Repository, Depends(MainRepository)],
    current_active_user: Annotated[User, Depends(get_current_active_user)],
):
    return repository.create_wta_event(event, user_id)


@app.get("/users/{user_id}/events/", response_model=list[WTAEvent])
def get_events(
    user_id: int,
    repository: Repository = Depends(MainRepository),
    current_active_user: User = Depends(get_current_active_user),
):
    return repository.get_wta_events(user_id)


@app.post(f"/{settings.auth_url}", response_model=Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    repository: Annotated[Repository, Depends(MainRepository)],
):
    user = repository.authenticate_user(
        username=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(
        minutes=settings.access_token_expire_minutes,
    )
    access_token = repository.create_access_token(
        data={
            "sub": user.username,
            "id": user.id,
        },
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


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
