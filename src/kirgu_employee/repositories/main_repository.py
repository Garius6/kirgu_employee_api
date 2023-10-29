from abc import ABC, abstractmethod
from datetime import timedelta, datetime
from sqlalchemy.orm import Session

from kirgu_employee.settings import settings
from ..database.databese import SessionLocal
from jose import jwt
from ..schemas import UserCreate, User, UserInDb, WTAEventCreate
from ..database import models
from passlib.context import CryptContext


ALGORITHM = "HS256"


class Repository(ABC):
    @abstractmethod
    def create_user(self, user: UserCreate) -> int:
        pass

    @abstractmethod
    def get_users(self) -> list[models.User]:
        pass

    @abstractmethod
    def create_wta_event(self, event: WTAEventCreate, user_id: int) -> int:
        pass

    @abstractmethod
    def get_wta_events(
        self, user_id: int
    ) -> list[models.WorkingTimeAccountingSystemEvent]:
        pass

    @abstractmethod
    def get_user(self, username: str) -> User:
        pass

    @abstractmethod
    def authenticate_user(self, username: str, password: str):
        pass

    @abstractmethod
    def create_access_token(
        self,
        data: dict,
        expires_delta: timedelta | None = None,
    ):
        pass


class MainRepository(Repository):
    def __init__(self):
        self._pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    def create_user(
        self,
        user: UserCreate,
        db: Session = SessionLocal(),
    ):
        hashed_password = self._get_password_hash(user.password)
        db_user = models.User(
            username=user.username,
            hashed_password=hashed_password,
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user.id

    def get_users(
        self,
        db: Session = SessionLocal(),
        skip: int = 0,
        limit: int = 100,
    ) -> list[models.User]:
        users = db.query(models.User).offset(skip).limit(limit).all()
        return users

    def create_wta_event(
        self,
        event: WTAEventCreate,
        user_id: int,
        db: Session = SessionLocal(),
    ):
        db_wta = models.WorkingTimeAccountingSystemEvent(
            user_id=user_id,
            date=event.date,
        )  # type: ignore
        db.add(db_wta)
        db.commit()
        db.refresh(db_wta)
        return db_wta.id

    def get_wta_events(
        self,
        user_id: int,
        skip: int = 0,
        limit: int = 100,
        db: Session = SessionLocal(),
    ) -> list[models.WorkingTimeAccountingSystemEvent]:
        events = (
            db.query(models.WorkingTimeAccountingSystemEvent)
            .where(models.WorkingTimeAccountingSystemEvent.user_id == user_id)
            .order_by(models.WorkingTimeAccountingSystemEvent.date)
            .offset(skip)
            .limit(limit)
            .all()
        )
        return events

    def get_user(
        self,
        username: str,
        db: Session = SessionLocal(),
    ) -> UserInDb | None:
        user = db.query(models.User).filter(models.User.username == username).first()
        if user is None:
            return None
        return user

    def authenticate_user(self, username: str, password: str):
        user = self.get_user(username=username)
        if not user:
            return False
        if not self._verify_password(password, user.hashed_password):
            return False

        return user

    def _verify_password(self, password: str, hashed_password: str):
        return self._pwd_context.verify(password, hashed_password)

    def _get_password_hash(self, password: str):
        return self._pwd_context.hash(password)

    def create_access_token(
        self,
        data: dict,
        expires_delta: timedelta | None = None,
    ):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(
            to_encode,
            settings.secret_key,
            algorithm=ALGORITHM,
        )
        return encoded_jwt
