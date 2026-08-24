import time

import pytest

from config import ADMIN_URL
from Common.DB import query_one

ERP = f"{ADMIN_URL}/admin-api/erp"


def _unique(prefix="AT"):
    return f"{prefix}{int(time.time() * 1000)}"


def _assert_ok(resp):
    assert resp.status_code == 200, f"HTTP {resp.status_code}:\n{resp.text[:500]}"
    r = resp.json()
    assert r["code"] == 0, f"业务失败: code={r.get('code')}, msg={r.get('msg', '')}"
    return r


def _resp_id(r):
    data = r["data"]
    assert data is not None, f"接口返回 data 为 None: {r}"
    return data if isinstance(data, (int, str)) else data.get("id")


def _cleanup(api_session, auth_headers, path, data_id):
    try:
        resp = api_session.delete(f"{ERP}{path}", params={"id": data_id}, headers=auth_headers)
        _assert_ok(resp)
        print(f"[cleanup] {path} id={data_id} 删除成功")
    except Exception as e:
        print(f"[cleanup] {path} id={data_id} 删除失败: {e}")


@pytest.fixture(scope="session")
def production_product(api_session, auth_headers):
    """自建产品（含产品分类 + 产品单位）→ 返回产品 id → 逆序删除"""
    r = _assert_ok(api_session.post(f"{ERP}/product-category/create", json={
        "parentId": 0, "name": _unique("产品分类"), "code": _unique("CAT"),
        "sort": 10, "status": 1,
    }, headers=auth_headers))
    category_id = _resp_id(r)
    #r = _assert_ok(api_session.post(f"{ERP}/product-unit/create", json={
    #    "name": _unique("产品单位"), "status": 1,          #业务逻辑上只用"name": "KG" 暂不新建单位
    #}, headers=auth_headers))
    unit_id = "2047529099331428353"
    r = _assert_ok(api_session.post(f"{ERP}/product/create", json={
        "name": _unique("生产产品"), "barCode": _unique("BAR"),
        "categoryId": category_id, "unitId": unit_id, "status": 1,
    }, headers=auth_headers))
    product_id = _resp_id(r)
    print(f"[Fixture] category_id={category_id} unit_id={unit_id} product_id={product_id}")
    yield product_id
    _cleanup(api_session, auth_headers, "/product/delete", product_id)
    #_cleanup(api_session, auth_headers, "/product-unit/delete", unit_id)
    _cleanup(api_session, auth_headers, "/product-category/delete", category_id)


@pytest.fixture(scope="session")
def production_type_create(api_session, auth_headers, production_product):
    """自建生产类型（依赖真实产品）→ 返回生产类型 id → 删除"""
    product_id = production_product
    r = _assert_ok(api_session.post(f"{ERP}/production-type/create", json={
        "name": _unique("生产类型"),
        "status": 0,
        "remark": "autotest",
        "materialProductIds": [product_id],
        "productProductIds": [product_id],
    }, headers=auth_headers))
    type_id = _resp_id(r)
    print(f"[Fixture] production_type_id = {type_id}")
    yield type_id
    _cleanup(api_session, auth_headers, "/production-type/delete", type_id)


@pytest.fixture(scope="session")
def production_plan_create(api_session, auth_headers, production_type_create, production_product):
    """自建生产计划（依赖真实生产类型 + 产品）→ 返回计划 id → 删除"""
    type_id = production_type_create
    product_id = production_product
    body = {
        "id": 0,
        "title": _unique("生产计划"),
        "productionTypeId": type_id,
        "productionTypeName": _unique("生产类型"),
        "targetQuantity": 1000,
        "remark": "autotest",
        "productIds": [product_id],
    }
    try:
        r = _assert_ok(api_session.get(f"{ERP}/warehouse/simple-list", headers=auth_headers))
        items = r["data"] or []
        center = next((w for w in items if w.get("operationCenterId")), None)
        if center:
            body["centerId"] = center["operationCenterId"]
            body["centerName"] = center.get("operationCenterName", "")
    except Exception as e:
        print(f"[Fixture] 获取分拣中心失败(忽略，centerId 非必传): {e}")
    r = _assert_ok(api_session.post(f"{ERP}/production-plan/create", json=body, headers=auth_headers))
    row = query_one("SELECT id FROM erp_production_plan WHERE title=%s", (body["title"],))
    assert row, f"DB 未查到生产计划 {body['title']}"
    plan_id = row["id"]
    print(f"[Fixture] production_plan_id = {plan_id}")
    yield plan_id
    try:
        api_session.put(f"{ERP}/production-plan/update-status", json={"id": plan_id, "status": 50}, headers=auth_headers)
    except Exception as e:
        print(f"[cleanup] 生产计划置为已取消失败 {plan_id}: {e}")
    _cleanup(api_session, auth_headers, "/production-plan/delete", plan_id)
