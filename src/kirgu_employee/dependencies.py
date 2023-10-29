from typing import Annotated

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext

from kirgu_employee.repositories.main_repository import MainRepository, Repository
from kirgu_employee.schemas import User
from kirgu_employee.settings import settings

from .database.databese import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl=settings.auth_url)


def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    repository: Annotated[Repository, Depends(MainRepository)],
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(token, settings.secret_key, algorithms=["HS256"])
        username: str = payload.get("sub")  # type: ignore
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception
    user = repository.get_user(username=username)
    if user is None:
        raise credentials_exception
    return user


def get_current_active_user(current_user: Annotated[User, Depends(get_current_user)]):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user
