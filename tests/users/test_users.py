import pytest
import json
from random import choice

from fastapi.testclient import TestClient

from wapang.app.users.models import User

# TEST POST /api/users
def test_signup(
    client: TestClient
):
    req = {
        "email": "test1234@snu.ac.kr",
        "password": "password123"
    }

    res = client.post("/users", json=req)
    res_json = res.json()
    
    assert res.status_code == 201
    assert res_json["id"] is not None
    assert res_json["email"] == "test1234@snu.ac.kr"
    
    # 로그인 테스트
    res = client.post("/auth/tokens", json=req)
    res_json = res.json()
    
    assert res.status_code == 200

def test_signup_missing_email(
    client: TestClient
):
    req = {
        "password": "password123"
    }

    res = client.post("/users", json=req)
    res_json = res.json()
    
    assert res.status_code == 400
    assert res_json["error_code"] == "ERR_002"
    assert res_json["error_msg"] == "MISSING REQUIRED FIELDS"

def test_signup_missing_password(
    client: TestClient
):
    req = {
        "email": "test1234@snu.ac.kr"
    }

    res = client.post("/users", json=req)
    res_json = res.json()
    
    assert res.status_code == 400
    assert res_json["error_code"] == "ERR_002"
    assert res_json["error_msg"] == "MISSING REQUIRED FIELDS"

def test_signup_invalid_email(
    client: TestClient
):
    req = {
        "email": "test.snu.ac.kr",
        "password": "password123"
    }

    res = client.post("/users", json=req)
    res_json = res.json()
    
    assert res.status_code == 400
    assert res_json["error_code"] == "ERR_003"
    assert res_json["error_msg"] == "INVALID FIELD FORMAT"

def test_signup_short_password(
    client: TestClient
):
    req = {
        "email": "test1234@snu.ac.kr",
        "password": "short"
    }

    res = client.post("/users", json=req)
    res_json = res.json()
    
    assert res.status_code == 400
    assert res_json["error_code"] == "ERR_003"
    assert res_json["error_msg"] == "INVALID FIELD FORMAT"

def test_signup_long_password(
    client: TestClient
):
    req = {
        "email": "test1234@snu.ac.kr",
        "password": "longpasswordlongpassword"
    }

    res = client.post("/users", json=req)
    res_json = res.json()
    
    assert res.status_code == 400
    assert res_json["error_code"] == "ERR_003"
    assert res_json["error_msg"] == "INVALID FIELD FORMAT"


def test_signup_email_conflict(
    client: TestClient,
    user: User
):
    req = {
        "email": "test1234@snu.ac.kr",
        "password": "password321"
    }

    res = client.post("/users", json=req)
    res_json = res.json()

    assert res.status_code == 409
    assert res_json["error_code"] == "ERR_004"
    assert res_json["error_msg"] == "EMAIL ALREADY EXISTS"
    
# TEST GET /api/users/me
def test_get_me(
    client: TestClient,
    access_token: str
):
    auth_header = {"Authorization": f"Bearer {access_token}"}
    
    res = client.get("/users/me", headers=auth_header)
    
    assert res.status_code == 200
    
def test_get_me_without_header(
    client: TestClient
):
    res = client.get("/users/me")
    res_json = res.json()
    
    assert res.status_code == 401
    assert res_json["error_code"] == "ERR_005"
    assert res_json["error_msg"] == "UNAUTHENTICATED"
    
def test_get_me_invalid_header(
    client: TestClient,
    access_token: str
):
    invalid_header = {"Authorization": f"{access_token}"}
    
    res = client.get("/users/me", headers=invalid_header)
    res_json = res.json()
    
    assert res.status_code == 400
    assert res_json["error_code"] == "ERR_006"
    assert res_json["error_msg"] == "BAD AUTHORIZATION HEADER"
    
def test_get_me_invalid_token(
    client: TestClient,
):
    auth_header = {"Authorization": f"Bearer invalidtoken"}
    
    res = client.get("/users/me", headers=auth_header)
    res_json = res.json()
    
    assert res.status_code == 401
    assert res_json["error_code"] == "ERR_007"
    assert res_json["error_msg"] == "INVALID TOKEN"

# TEST PATCH /api/users/me
def test_patch_me(
    client: TestClient,
    access_token: str
):
    auth_header = {"Authorization": f"Bearer {access_token}"}
    req = {
        "nickname": "waffle",
        "address": "Seoul"
    }

    res = client.patch("/users/me", headers=auth_header, json=req)
    res_json=res.json()

    assert res.status_code == 200
    assert res_json["nickname"] == req["nickname"]
    assert res_json["address"] == req["address"]

def test_patch_me_random(
    client: TestClient,
    access_token: str
):
    auth_header = {"Authorization": f"Bearer {access_token}"}
    possible = {
        "nickname": "waffle",
        "address": "Seoul",
        "phone_number": "010-0000-1111"
    }
    to_update = choice(list(possible.keys()))
    req = {
        to_update: possible[to_update]
    }
    print(to_update)
    res = client.patch("/users/me", headers=auth_header, json=req)
    res_json=res.json()

    assert res.status_code == 200
    assert res_json[to_update] == req[to_update]

def test_patch_me_invalid_req(
    client: TestClient,
    access_token: str
):
    auth_header = {"Authorization": f"Bearer {access_token}"}
    req = {
        "invalid": "content"
    }

    res = client.patch("/users/me", headers=auth_header, json=req)
    res_json=res.json()

    assert res.status_code == 400
    assert res_json["error_code"] == "ERR_003"
    assert res_json["error_msg"] == "INVALID FIELD FORMAT"

def test_patch_me_without_token(
    client: TestClient
):
    req = {
        "nickname": "waffle"
    }

    res = client.patch("/users/me", json=req)
    res_json=res.json()

    assert res.status_code == 401
    assert res_json["error_code"] == "ERR_005"
    assert res_json["error_msg"] == "UNAUTHENTICATED"
    
# TEST GET /api/users/me/orders
def test_get_me_orders(
    client: TestClient,
    access_token: str,
    orders
):
    auth_header = {"Authorization": f"Bearer {access_token}"}

    res = client.get("/users/me/orders", headers=auth_header)
    res_json = res.json()

    assert res.status_code == 200
    assert len(res_json) == 3
    for i in range(3):
        assert res_json[i]["order_id"] is not None

# TEST GET /api/users/me/reviews
def test_get_me_reviews(
    client: TestClient,
    access_token: str,
    reviews
):
    auth_header = {"Authorization": f"Bearer {access_token}"}

    res = client.get("/users/me/reviews", headers=auth_header)
    res_json = res.json()

    assert res.status_code == 200
    assert len(res_json) == 1
    assert res_json[0]["item_name"] == "item0"
    assert res_json[0]["rating"] == 3
    assert res_json[0]["comment"] == "good"