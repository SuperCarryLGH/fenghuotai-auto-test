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
def app_product(api_session, auth_headers):
    """自建产品（含产品分类 + 产品单位）→ 返回产品 id → 逆序删除"""
    r = _assert_ok(api_session.post(f"{ERP}/product-category/create", json={
        "parentId": 0, "name": _unique("分类"), "code": _unique("CAT"),
        "sort": 10, "status": 1,
    }, headers=auth_headers))
    category_id = _resp_id(r)
    r = _assert_ok(api_session.post(f"{ERP}/product-unit/create", json={
        "name": _unique("单位"), "status": 1,
    }, headers=auth_headers))
    unit_id = _resp_id(r)
    r = _assert_ok(api_session.post(f"{ERP}/product/create", json={
        "name": _unique("产品"), "barCode": _unique("BAR"),
        "categoryId": category_id, "unitId": unit_id, "status": 1,
    }, headers=auth_headers))
    product_id = _resp_id(r)
    print(f"[Fixture] category_id={category_id} unit_id={unit_id} product_id={product_id}")
    yield product_id
    _cleanup(api_session, auth_headers, "/product/delete", product_id)
    _cleanup(api_session, auth_headers, "/product-unit/delete", unit_id)
    _cleanup(api_session, auth_headers, "/product-category/delete", category_id)


@pytest.fixture
def app_production_type(api_session, auth_headers, app_product):
    """自建生产类型（依赖产品）→ 返回生产类型 id → 删除"""
    product_id = app_product
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


@pytest.fixture
def app_production_plan(api_session, auth_headers, app_production_type, app_product):
    """自建生产计划（依赖生产类型 + 产品）→ 返回计划 id → 删除"""
    type_id = app_production_type
    product_id = app_product
    body = {
        "id": 0,
        "title": _unique("生产计划"),
        "productionTypeId": type_id,
        "productionTypeName": "",
        "targetQuantity": 1000,
        "remark": "autotest",
        "productIds": [product_id],
    }
    r = _assert_ok(api_session.post(f"{ERP}/production-plan/create", json=body, headers=auth_headers))
    plan_id = _resp_id(r)
    print(f"[Fixture] production_plan_id = {plan_id}")
    yield plan_id
    _cleanup(api_session, auth_headers, "/production-plan/delete", plan_id)


@pytest.fixture
def app_production_task(api_session, auth_headers, app_production_plan):
    """自建生产任务（依赖生产计划）→ 返回任务 id → 删除"""
    plan_id = app_production_plan
    body = {
        "planId": plan_id,
        "workerCount": 5,
        "remark": "autotest",
        "taskStartTime": time.strftime("%Y-%m-%d 08:00:00", time.localtime()),
        "taskEndTime": time.strftime("%Y-%m-%d 18:00:00", time.localtime()),
    }
    r = _assert_ok(api_session.post(f"{ERP}/app-production-task/create", json=body, headers=auth_headers))
    task_id = _resp_id(r)
    print(f"[Fixture] production_task_id = {task_id}")
    yield task_id
    _cleanup(api_session, auth_headers, "/production-task/delete", task_id)
