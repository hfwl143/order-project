import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

import main
from database import Base, get_db


@pytest.fixture
def client():
    engine = create_engine(
        "sqlite://",
        connect_args={"check_same_thread": False},
        poolclass=StaticPool,
    )
    Base.metadata.create_all(bind=engine)
    testing_session = sessionmaker(bind=engine, autoflush=False)

    def override_get_db():
        db = testing_session()
        try:
            yield db
        finally:
            db.close()

    main.app.dependency_overrides[get_db] = override_get_db
    try:
        yield TestClient(main.app)
    finally:
        main.app.dependency_overrides.pop(get_db, None)
        engine.dispose()


def register(client: TestClient, username: str) -> str:
    response = client.post(
        "/api/register",
        json={"username": username, "password": "secret123"},
    )
    assert response.status_code == 200
    return response.json()["access_token"]


def auth(token: str) -> dict[str, str]:
    return {"Authorization": f"Bearer {token}"}


def test_health_endpoints_are_mounted(client: TestClient):
    assert client.get("/api/").json() == {"message": "Hello from backend"}
    assert client.get("/api/health").json() == {"status": "ok"}


def test_registration_login_and_auth_errors(client: TestClient):
    short_password = client.post(
        "/api/register",
        json={"username": "short-pass", "password": "123"},
    )
    assert short_password.status_code == 400

    token = register(client, "publisher")
    duplicate = client.post(
        "/api/register",
        json={"username": "publisher", "password": "secret123"},
    )
    assert duplicate.status_code == 400

    login = client.post(
        "/api/login",
        data={"username": "publisher", "password": "secret123"},
    )
    assert login.status_code == 200
    assert login.json()["access_token"]
    assert login.json()["token_type"] == "bearer"

    bad_login = client.post(
        "/api/login",
        data={"username": "publisher", "password": "incorrect"},
    )
    assert bad_login.status_code == 401
    assert client.get("/api/orders", headers=auth("invalid-token")).status_code == 401
    assert client.get("/api/orders").status_code == 401
    assert token


def test_order_workflow_and_permissions(client: TestClient):
    publisher_token = register(client, "publisher")
    taker_token = register(client, "taker")

    order_data = {
        "title": "API 测试任务",
        "description": "完成接口测试",
        "tag": "编程",
        "deadline": "2026-12-31 18:00",
    }
    created = client.post(
        "/api/orders", json=order_data, headers=auth(publisher_token)
    )
    assert created.status_code == 200
    order = created.json()
    order_id = order["id"]
    assert order["order_status"] == "未接单"
    assert order["publisher_id"]

    assert client.post("/api/orders", json=order_data).status_code == 401
    assert client.post(
        "/api/orders",
        json={**order_data, "tag": "unknown"},
        headers=auth(publisher_token),
    ).status_code == 422

    hall = client.get("/api/orders", headers=auth(taker_token))
    assert hall.status_code == 200
    assert [item["id"] for item in hall.json()] == [order_id]
    assert client.get(
        "/api/orders?tag=绘图", headers=auth(taker_token)
    ).json() == []
    assert client.get(
        "/api/orders/mine?role=invalid", headers=auth(publisher_token)
    ).status_code == 400

    own_take = client.post(
        f"/api/orders/{order_id}/take", headers=auth(publisher_token)
    )
    assert own_take.status_code == 403

    taken = client.post(
        f"/api/orders/{order_id}/take", headers=auth(taker_token)
    )
    assert taken.status_code == 200
    assert taken.json()["order_status"] == "已接单"
    assert client.get("/api/orders", headers=auth(publisher_token)).json() == []

    edit_taken = client.put(
        f"/api/orders/{order_id}",
        json=order_data,
        headers=auth(publisher_token),
    )
    assert edit_taken.status_code == 400

    abandon = client.post(
        f"/api/orders/{order_id}/abandon", headers=auth(taker_token)
    )
    assert abandon.status_code == 200
    agreed = client.post(
        f"/api/orders/{order_id}/abandon/agree",
        headers=auth(publisher_token),
    )
    assert agreed.status_code == 200
    assert agreed.json()["order_status"] == "未接单"
    assert agreed.json()["abandon_requested"] is False

    closed = client.post(
        f"/api/orders/{order_id}/close", headers=auth(publisher_token)
    )
    assert closed.status_code == 200
    assert client.get("/api/orders", headers=auth(taker_token)).json() == []