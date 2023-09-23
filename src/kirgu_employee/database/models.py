from sqlalchemy import Column, ForeignKey, Integer, String, Boolean, Date, Time
from sqlalchemy.orm import relationship
from .databese import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    wta_events = relationship(
        "WorkingTimeAccountingSystemEvent",
        back_populates="user",
    )


class WorkingTimeAccountingSystemEvent(Base):
    __tablename__ = "working_time_accounting_system_event"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))

    date = Column(Date, nullable=False)
    time = Column(Time, nullable=False)

    user = relationship("User", back_populates="wta_events")
