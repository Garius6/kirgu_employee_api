import datetime
from fastapi.testclient import TestClient

from kirgu_employee.repositories.main_repository import MainRepository, Repository
from kirgu_employee.schemas import User, UserCreate, WTAEvent, WTAEventCreate
from .main import app


class TestRepository(Repository):
    def create_user(self, user: UserCreate) -> int:
        return 1

    def create_wta_event(self, event: WTAEventCreate) -> int:
        return 1

    def get_users(self) -> list[User]:
        return [User(username="test1", is_active=True, id=1)]

    def get_wta_events(self) -> list[WTAEvent]:
        current_date = datetime.datetime.now()
        return [
            WTAEvent(
                id=1,
                time=current_date.time(),
                date=current_date.date(),
                user_id=1,
            )
        ]


app.dependency_overrides[MainRepository] = TestRepository
app.debug = True
client = TestClient(app)


def test_healthcheck():
    response = client.get("/healthcheck")
    assert response.status_code == 200
    assert response.json() == "ok"


def test_create_user():
    response = client.post(
        "/users/",
        json={"username": "test", "password": "123"},
    )
    assert response.status_code == 201


def test_get_users():
    response = client.get("/users/")
    assert response.status_code == 200


def test_get_events():
    response = client.get("/events/")
    assert response.status_code == 200


def test_create_event():
    current_date = datetime.datetime.now()
    response = client.post(
        "/events/",
        json={
            "time": current_date.time().isoformat(),
            "date": current_date.date().isoformat(),
        },
    )
    assert response.status_code == 201
