import time

import pytest

from config import APP_URL

ERP = f"{APP_URL}/admin-api/erp"


def _unique(prefix="AT"):
    return f"{prefix}{int(time.time() * 1000)}"


def _assert_ok(resp):
    assert resp.status_code == 200, f"HTTP {resp.status_code}:\n{resp.text[:500]}"
    r = resp.json()
    assert r["code"] == 0, f"业务失败: code={r.get('code')}, msg={r.get('msg', '')}"
    return r


def _resp_id(r):
    data = r["data"]
    if isinstance(data, dict):
        return data.get("id") or data.get("data")
    return data


def _cleanup(api_session, auth_headers, path, data_id):
    try:
        resp = api_session.delete(f"{ERP}{path}", params={"id": data_id}, headers=auth_headers)
        _assert_ok(resp)
        print(f"[cleanup] {path} id={data_id} 删除成功")
    except Exception as e:
        print(f"[cleanup] {path} id={data_id} 删除失败: {e}")


@pytest.fixture
def app_auction_round(api_session, auth_headers):
    """自建竞拍场次 → 返回场次 id → 删除"""
    body = {
        "id": 0,
        "auctionName": _unique("竞拍场次"),
        "auctionType": 1,
        "startTime": "",
        "endTime": "",
        "coverImage": "",
        "description": "autotest",
        "status": 1,
        "remark": "autotest",
        "items": [],
    }
    r = _assert_ok(api_session.post(f"{ERP}/auction-round/create", json=body, headers=auth_headers))
    round_id = _resp_id(r)
    print(f"[Fixture] auction_round_id = {round_id}")
    yield round_id
    try:
        resp = api_session.delete(f"{ERP}/auction-round/delete", params={"ids": [round_id]}, headers=auth_headers)
        _assert_ok(resp)
        print(f"[cleanup] auction-round id={round_id} 删除成功")
    except Exception as e:
        print(f"[cleanup] auction-round id={round_id} 删除失败: {e}")


@pytest.fixture
def app_auction_round_item(api_session, auth_headers, app_auction_round):
    """自建竞拍商品（依赖竞拍场次）→ 返回商品 id → 删除"""
    round_id = app_auction_round
    body = {
        "id": 0,
        "roundId": round_id,
        "productId": 1,
        "productCode": "SP001",
        "productName": "商品A",
        "itemName": "商品A",
        "productCategoryId": 1,
        "productCategoryName": "分类A",
        "productUnitId": 1,
        "productUnitName": "KG",
        "availableStock": 1000,
        "packageCount": 10,
        "operationCenterId": 1,
        "operationCenterName": "分拣中心A",
        "productCoverImage": "",
        "productCarouselImages": [],
        "totalQuantity": 500,
        "startPrice": 10,
        "qualityLevel": "A",
        "initialBidCount": 0,
        "itemDescription": "",
        "sort": 0,
        "remark": "autotest",
    }
    r = _assert_ok(api_session.post(f"{ERP}/auction-round/item-create", json=body, headers=auth_headers))
    item_id = _resp_id(r)
    print(f"[Fixture] auction_round_item_id = {item_id}")
    yield item_id
    _cleanup(api_session, auth_headers, "/auction-round/item-delete", item_id)
