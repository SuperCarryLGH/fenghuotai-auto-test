import time

import pytest

from config import ADMIN_URL

ERP = f"{ADMIN_URL}/admin-api/erp"


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
    """从创建接口响应中提取 ID（兼容 data 为数字或对象两种返回）"""
    data = r["data"]
    assert data is not None, f"接口返回 data 为 None: {r}"
    return data if isinstance(data, (int, str)) else data.get("id")


def _cleanup(api_session, auth_headers, path, data_id):
    """统一后置清理：DELETE 接口 + id 参数"""
    try:
        resp = api_session.delete(f"{ERP}{path}", params={"id": data_id}, headers=auth_headers)
        _assert_ok(resp)
        print(f"[cleanup] {path} id={data_id} 删除成功")
    except Exception as e:
        print(f"[cleanup] {path} id={data_id} 删除失败: {e}")


@pytest.fixture
def autotest_supplier(api_session, auth_headers):
    """自建供应商 → 返回 id → 删除"""
    body = {
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
    r = _assert_ok(api_session.post(f"{ERP}/supplier/create", json=body, headers=auth_headers))
    supplier_id = _resp_id(r)
    print(f"[Fixture] supplier_id = {supplier_id}")
    yield supplier_id
    _cleanup(api_session, auth_headers, "/supplier/delete", supplier_id)


@pytest.fixture
def autotest_product(api_session, auth_headers):
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
def autotest_purchase_plan(api_session, auth_headers, autotest_product):
    """自建采购计划（依赖产品）→ 返回 id → 删除"""
    product_id = autotest_product
    body = {
        "title": _unique("采购计划"),
        "targetQuantity": 100,
        "status": 10,
        "items": [{"productId": product_id, "targetQuantity": 100}],
    }
    r = _assert_ok(api_session.post(f"{ERP}/purchase-plan/create", json=body, headers=auth_headers))
    plan_id = _resp_id(r)
    print(f"[Fixture] purchase_plan_id = {plan_id}")
    yield plan_id
    _cleanup(api_session, auth_headers, "/purchase-plan/delete", plan_id)


@pytest.fixture
def autotest_purchase_order(api_session, auth_headers, autotest_supplier, autotest_product, autotest_purchase_plan):
    """自建采购订单（依赖供应商/产品/采购计划；分拣中心=3、运输方式=平台运输）→ 返回 id → 删除"""
    supplier_id = autotest_supplier
    product_id = autotest_product
    plan_id = autotest_purchase_plan
    body = {
        "purchasePlanId": plan_id,
        "supplierId": supplier_id,
        "vendorId": supplier_id,
        "deliveryCenterId": 3,
        "erpPurchaseOrderItemReqVOList": [
            {"productId": product_id, "productName": "", "productPrice": 100, "count": 10}
        ],
        "totalProductPrice": 1000,
        "totalPrice": 1000,
        "paymentMethod": 10,
        "transportMethod": 20,
        "transportTypeId": 20,
        "transportTypeName": "平台运输",
    }
    r = _assert_ok(api_session.post(f"{ERP}/app-purchase-order/create", json=body, headers=auth_headers))
    order_id = _resp_id(r)
    print(f"[Fixture] purchase_order_id = {order_id}")
    yield order_id
    _cleanup(api_session, auth_headers, "/purchase-order/delete", order_id)


@pytest.fixture
def autotest_purchase_in(api_session, auth_headers, autotest_purchase_order, autotest_product):
    """自建采购入库（依赖采购订单 + 产品）→ 返回 id → 删除"""
    order_id = autotest_purchase_order
    product_id = autotest_product
    body = {
        "id": 0,
        "accountId": 1,
        "inTime": time.strftime("%Y-%m-%d %H:%M:%S"),
        "orderId": order_id,
        "discountPercent": 100,
        "otherPrice": 0,
        "fileUrl": "",
        "remark": "",
        "items": [
            {
                "id": 0,
                "warehouseId": 3,
                "warehouseName": "分拣1仓",
                "productId": product_id,
                "productPrice": 100,
                "itemCode": "",
                "itemDetailId": 0,
            }
        ],
    }
    r = _assert_ok(api_session.post(f"{ERP}/purchase-in/create", json=body, headers=auth_headers))
    in_id = _resp_id(r)
    print(f"[Fixture] purchase_in_id = {in_id}")
    yield in_id
    _cleanup(api_session, auth_headers, "/purchase-in/delete", in_id)
