from sqlalchemy.orm import Session
from src.database.databese import SessionLocal

from ..schemas import UserCreate, User, WTAEvent, WTAEventCreate
from ..database import models


class MainRepository:
    def create_user(
        self,
        user: UserCreate,
        db: Session = SessionLocal(),
    ):
        hashed_password = user.password + "nigger"
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
        limit: int = 0,
    ) -> list[User]:
        users = db.query(models.User).offset(skip).limit(limit).all()
        return [User(**user) for user in users]

    def create_wta_event(
        self,
        event: WTAEventCreate,
        db: Session = SessionLocal(),
    ):
        db_wta = models.WorkingTimeAccountingSystemEvent(
            time=event.time,
            date=event.date,
        )  # type: ignore
        db.add(db_wta)
        db.commit()
        db.refresh(db_wta)
        return db_wta.id

    def get_wta_events(
        self, db: Session = SessionLocal(), skip: int = 0, limit: int = 100
    ) -> list[WTAEvent]:
        events = (
            db.query(models.WorkingTimeAccountingSystemEvent)
            .offset(skip)
            .limit(limit)
            .order_by(models.WorkingTimeAccountingSystemEvent.date)
            .all()
        )
        return [WTAEvent(**event) for event in events]
