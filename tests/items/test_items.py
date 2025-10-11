from fastapi.testclient import TestClient

def test_create_item(
    client: TestClient,
    access_token: str,
    store: dict,
    item_create_request: dict
):
    res = client.post("/items", json=item_create_request, headers={"Authorization": f"Bearer {access_token}"})
    res_json = res.json()
    assert res.status_code == 201
    assert res_json["item_name"] == item_create_request["item_name"]
    assert res_json["price"] == item_create_request["price"]
    assert res_json["stock"] == item_create_request["stock"]

def test_create_item_missing_field(
    client: TestClient,
    access_token: str,
    store: dict,
):
    req = {
        "item_name": "초콜릿",
        "price": 5000
    }
    res = client.post("/items", json=req, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 400
    assert res.json()["error_code"] == "ERR_002"
    assert res.json()["error_msg"] == "MISSING REQUIRED FIELDS"

def test_create_item_with_long_item_name(
    client: TestClient,
    access_token: str,
    store: dict,
):
    req = {
        "item_name": "A" * 51,
        "price": 5000,
        "stock": 20
    }
    res = client.post("/items", json=req, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 400
    assert res.json()["error_code"] == "ERR_003"
    assert res.json()["error_msg"] == "INVALID FIELD FORMAT"

def test_create_item_with_negative_price(
    client: TestClient,
    access_token: str,
    store: dict,
):
    req = {
        "item_name": "초콜릿",
        "price": -5000,
        "stock": 20
    }
    res = client.post("/items", json=req, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 400
    assert res.json()["error_code"] == "ERR_003"
    assert res.json()["error_msg"] == "INVALID FIELD FORMAT"

def test_create_item_with_negative_stock(
    client: TestClient,
    access_token: str,
    store: dict,
):
    req = {
        "item_name": "초콜릿",
        "price": 5000,
        "stock": -20
    }
    res = client.post("/items", json=req, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 400
    assert res.json()["error_code"] == "ERR_003"
    assert res.json()["error_msg"] == "INVALID FIELD FORMAT"


def test_create_item_with_no_store(
    client: TestClient,
    access_token: str,
):
    req = {
        "item_name": "초콜릿",
        "price": 5000,
        "stock": 20
    }
    res = client.post("/items", json=req, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 403
    assert res.json()["error_code"] == "ERR_011"
    assert res.json()["error_msg"] == "NO STORE OWNED"

def test_patch_item(
    client: TestClient,
    access_token: str,
    item: dict
):
    req = {
        "item_name": "쿠키",
        "price": 6000,
        "stock": 30
    }
    res = client.patch(f"/items/{item['id']}", json=req, headers={"Authorization": f"Bearer {access_token}"})
    res_json = res.json()
    assert res.status_code == 200
    assert res_json["item_name"] == req["item_name"]
    assert res_json["price"] == req["price"]
    assert res_json["stock"] == req["stock"]

def test_patch_item_with_long_item_name(
    client: TestClient,
    access_token: str,
    item: dict
):
    req = {
        "item_name": "A" * 51,
        "price": 6000,
        "stock": 30
    }
    res = client.patch(f"/items/{item['id']}", json=req, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 400
    assert res.json()["error_code"] == "ERR_003"
    assert res.json()["error_msg"] == "INVALID FIELD FORMAT"

def test_patch_item_with_negative_price(
    client: TestClient,
    access_token: str,
    item: dict
):
    req = {
        "item_name": "쿠키",
        "price": -6000,
        "stock": 30
    }
    res = client.patch(f"/items/{item['id']}", json=req, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 400
    assert res.json()["error_code"] == "ERR_003"
    assert res.json()["error_msg"] == "INVALID FIELD FORMAT"

def test_patch_item_with_negative_stock(
    client: TestClient,
    access_token: str,
    item: dict
):
    req = {
        "item_name": "쿠키",
        "price": 6000,
        "stock": -30
    }
    res = client.patch(f"/items/{item['id']}", json=req, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 400
    assert res.json()["error_code"] == "ERR_003"
    assert res.json()["error_msg"] == "INVALID FIELD FORMAT"

def test_patch_item_with_no_price(
    client: TestClient,
    access_token: str,
    item: dict
):
    req = {
        "item_name": "쿠키",
        "stock": 30
    }
    res = client.patch(f"/items/{item['id']}", json=req, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 200
    res_json = res.json()
    assert res_json["item_name"] == req["item_name"]
    assert res_json["price"] == item["price"]
    assert res_json["stock"] == req["stock"]

def test_patch_item_with_no_stock(
    client: TestClient,
    access_token: str,
    item: dict
):
    req = {
        "item_name": "쿠키",
        "price": 6000
    }
    res = client.patch(f"/items/{item['id']}", json=req, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 200
    res_json = res.json()
    assert res_json["item_name"] == req["item_name"]
    assert res_json["price"] == req["price"]
    assert res_json["stock"] == item["stock"]

def test_patch_item_with_no_item_name(
    client: TestClient,
    access_token: str,
    item: dict
):
    req = {
        "price": 6000,
        "stock": 30
    }
    res = client.patch(f"/items/{item['id']}", json=req, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 200
    res_json = res.json()
    assert res_json["item_name"] == item["item_name"]
    assert res_json["price"] == req["price"]
    assert res_json["stock"] == req["stock"]

def test_patch_item_not_found(
    client: TestClient,
    access_token: str,
    store: dict,
):
    req = {
        "item_name": "쿠키",
        "price": 6000,
        "stock": 30
    }
    res = client.patch(f"/items/9999", json=req, headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 404
    assert res.json()["error_code"] == "ERR_013"
    assert res.json()["error_msg"] == "ITEM NOT FOUND"

def test_patch_item_with_no_store(
    client: TestClient,
    another_user_access_token: str,
    item: dict
):
    req = {
        "item_name": "쿠키",
        "price": 6000,
        "stock": 30
    }
    res = client.patch(f"/items/{item['id']}", json=req, headers={"Authorization": f"Bearer {another_user_access_token}"})
    assert res.status_code == 403
    assert res.json()["error_code"] == "ERR_011"
    assert res.json()["error_msg"] == "NO STORE OWNED"

def test_patch_item_of_another_store(
    client: TestClient,
    another_user_access_token: str,
    item: dict,
    store_2: dict
):
    req = {
        "item_name": "쿠키",
        "price": 6000,
        "stock": 30
    }
    res = client.patch(f"/items/{item['id']}", json=req, headers={"Authorization": f"Bearer {another_user_access_token}"})
    assert res.status_code == 403
    assert res.json()["error_code"] == "ERR_014"
    assert res.json()["error_msg"] == "NOT YOUR ITEM"

def test_get_items(
    client: TestClient,
    items: dict,
    store: dict,
):
    query_params = {
        "store_id": store["id"],
        "min_price": 5000,
        "max_price": 9000,
        "in_stock": True,
    }

    res = client.get("/items", params=query_params)
    res_json = res.json()
    assert res.status_code == 200
    for item in res_json:
        assert item["price"] >= query_params["min_price"]
        assert item["price"] <= query_params["max_price"]
        assert item["stock"] > 0

def test_get_items_no_store(
    client: TestClient,
    items: dict
):
    query_params = {
        "store_id": "9999",
        "min_price": 5000,
        "max_price": 9000,
        "in_stock": True,
    }

    res = client.get("/items", params=query_params)
    res_json = res.json()
    assert res.status_code == 404
    assert res_json["error_code"] == "ERR_010"
    assert res_json["error_msg"] == "STORE NOT FOUND"

def test_delete_item(
    client: TestClient,
    access_token: str,
    item: dict
):
    res = client.delete(f"/items/{item['id']}", headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 204

def test_delete_item_not_found(
    client: TestClient,
    access_token: str,
    store: dict,
):
    res = client.delete(f"/items/9999", headers={"Authorization": f"Bearer {access_token}"})
    assert res.status_code == 404
    assert res.json()["error_code"] == "ERR_013"
    assert res.json()["error_msg"] == "ITEM NOT FOUND"

def test_delete_item_no_access(
    client: TestClient,
    item: dict,
    store: dict,
    store_2: dict,
    another_user_access_token: str,
):
    res = client.delete(f"/items/{item['id']}", headers={"Authorization": f"Bearer {another_user_access_token}"})
    assert res.status_code == 403
    assert res.json()["error_code"] == "ERR_014"
    assert res.json()["error_msg"] == "NOT YOUR ITEM"

def test_get_store_items(
    client: TestClient,
    store: dict,
    items: dict,
):
    store_id = store["id"]
    res = client.get(f"/stores/{store_id}/items")
    res_json = res.json()
    assert res.status_code == 200
    item_ids = {item['id'] for item in items}
    for item in res_json:
        assert item['id'] in item_ids
        assert item['item_name'] in {i['item_name'] for i in items}
        assert item['price'] in {i['price'] for i in items}
        assert item['stock'] in {i['stock'] for i in items}

def test_get_store_items_no_store(
    client: TestClient,
):
    res = client.get(f"/stores/9999/items")
    res_json = res.json()
    assert res.status_code == 404
    assert res_json["error_code"] == "ERR_010"
    assert res_json["error_msg"] == "STORE NOT FOUND"