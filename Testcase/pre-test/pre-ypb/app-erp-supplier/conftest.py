import time

import pytest

from config import APP_URL

ERP = f"{APP_URL}/admin-api/erp"


def _unique(prefix="AT"):
    return f"{prefix}{int(time.time() * 1000)}"


def _mobile():
    return "156" + str(int(time.time() * 1000) % 90000000 + 10000000)


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
def app_supplier(api_session, auth_headers):
    """自建 APP 供应商 → 返回 id → 删除"""
    body = {
        "id": 0,
        "name": _unique("供应商"),
        "legalName": _unique("企业"),
        "contact": _unique("联系人"),
        "mobile": _mobile(),
        "status": 1,
        "sort": 10,
        "taxNo": _unique("TAX"),
        "idCard": "110101199001011234",
        "supplierType": 10,
        "provinceCode": "110000",
        "cityCode": "110100",
        "districtCode": "110101",
        "province": "北京市",
        "city": "北京市",
        "district": "东城区",
        "detailAddress": "某某路 1 号",
    }
    r = _assert_ok(api_session.post(f"{ERP}/app-supplier/create", json=body, headers=auth_headers))
    supplier_id = _resp_id(r)
    print(f"[Fixture] app_supplier_id = {supplier_id}")
    yield supplier_id
    _cleanup(api_session, auth_headers, "/supplier/delete", supplier_id)
