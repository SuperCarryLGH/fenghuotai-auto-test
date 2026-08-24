import json
import time

import pytest

from config import APP_URL, ADMIN_URL
from Common.DB import query

ERP = f"{APP_URL}/admin-api/erp"

BUYER_ID = 2090281734832517121
BUYER_NAME = "autotest采购员"


def purchase_order_complete_shipping(api_session, buyer_headers, autotest_purchase_order):
    r = _assert_ok(api_session.post(f"{ERP}/app-purchase-order/complete-shipping",
                                    params={"id": autotest_purchase_order}, headers=buyer_headers))
    return r["data"]
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


def _b_login(api_session, mobile):
    """B端（system_users）短信登录，返回带鉴权的 headers"""
    r = api_session.post(f"{ADMIN_URL}/admin-api/system/auth/sms-login",
                         json={"mobile": mobile, "code": "9999"},
                         headers={"tenant-id": "1", "appId": "admin", "sign": "admin"})
    data = r.json()
    assert data["code"] == 0, f"B端登录失败 {mobile}: {data.get('msg', '')}"
    token = data["data"]["accessToken"]
    return {"tenant-id": "1", "appId": "admin", "sign": "admin",
            "Authorization": f"Bearer {token}"}


@pytest.fixture
def buyer_headers(api_session):
    """采购员（18700000000 / autotest采购员）"""
    return _b_login(api_session, "18700000000")


@pytest.fixture
def weigher_headers(api_session):
    """司磅（18600000003 / 张一）"""
    return _b_login(api_session, "18600000003")


@pytest.fixture
def inspector_headers(api_session):
    """质检员（18600000005 / 李志管）"""
    return _b_login(api_session, "18600000005")
@pytest.fixture
def autotest_supplier(api_session, auth_headers):
    """自建供应商 → 返回 id → 删除"""
    body = {
        "name": _unique("供应商"),
        "legalName":"autotest",
        "contact": _unique("联系人"),
        "mobile": _mobile(),
        "status": 1,
        "sort": 10,
        "idCard":"410101111111111111",
        "taxNo": _unique("TAX"),
        "buyerId": BUYER_ID,
        "buyerName": BUYER_NAME,
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
        "categoryId": category_id, "unitId": unit_id, "status": 2,
    }, headers=auth_headers))
    product_id = _resp_id(r)
    print(f"[Fixture] category_id={category_id} unit_id={unit_id} product_id={product_id}")
    yield product_id
    _cleanup(api_session, auth_headers, "/product/delete", product_id)
    _cleanup(api_session, auth_headers, "/product-unit/delete", unit_id)
    _cleanup(api_session, auth_headers, "/product-category/delete", category_id)


@pytest.fixture
def autotest_purchase_plan(api_session, auth_headers, autotest_product):
    """自建采购计划（依赖产品；先清理该采购员旧进行中计划避免区间冲突）→ 返回 id → 删除"""
    product_id = autotest_product
    # 清理该采购员已有的进行中计划（status 10/20/30），避免"同一采购员区间冲突"
    try:
        rows = query("SELECT id FROM erp_purchase_plan "
                     "WHERE deleted=0 AND status IN (10,20,30) AND buyer_commissioner_id=%s", (BUYER_ID,))
        for row in rows:
            api_session.delete(f"{ERP}/purchase-plan/delete", params={"id": row["id"]}, headers=auth_headers)
    except Exception as e:
        print(f"[Fixture] 清理旧采购计划失败: {e}")
    body = {
        "title": _unique("采购计划"),
        "targetQuantity": 100,
        "status": 10,
        "planDate": time.strftime("%Y-%m-%d"),
        "planEndDate": time.strftime("%Y-%m-%d"),
        "departmentId":108,
        "departmentName":"市场部门",
        "buyerCommissionerId": BUYER_ID,
        "buyerCommissionerName": BUYER_NAME,
        "items": [{"productId": product_id, "targetQuantity": 100}],
    }
    r = _assert_ok(api_session.post(f"{ERP}/purchase-plan/create", json=body, headers=auth_headers))
    plan_id = _resp_id(r)
    print(f"[Fixture] purchase_plan_id = {plan_id}")
    yield plan_id
    _cleanup(api_session, auth_headers, "/purchase-plan/delete", plan_id)


@pytest.fixture
def autotest_purchase_order(api_session, buyer_headers,auth_headers, autotest_supplier, autotest_product, autotest_purchase_plan):
    """自建采购订单（依赖供应商/产品/采购计划；采购员下单）→ 返回 id → 删除"""
    supplier_id = autotest_supplier
    product_id = autotest_product
    plan_id = autotest_purchase_plan
    body = {
        "id": 0,
        "purchasePlanId": plan_id,
        "supplierId": supplier_id,
        "supplierName": "", "supplierPhone": "", "supplierAddress": "",
        "vendorId": supplier_id,
        "vendorName": "", "vendorPhone": "", "vendorAddress": "",
        "deliveryCenterId": 2074701657159761922,  # autotest分拣中心
        "deliveryCenterName": "",
        "transportDistance": 100,
        "erpPurchaseOrderItemReqVOList": [
            {"orderId": 0, "productId": product_id, "productName": "", "barCode": "", "productPrice": 100, "count": 10}
        ],
        "totalProductPrice": 1000,
        "totalPrice": 1000,
        "paymentMethod": 10,
        "transportMethod": 20,
        "transportTypeId": 20,
        "transportTypeName": "平台运输",
        "transportFee": 200,
        "contractAttachments": "",
        "remark": "",
        "commissionerId": BUYER_ID,
        "commissionerName": BUYER_NAME,
        "commissionerPhone": "18700000000",
    }
    r = _assert_ok(api_session.post(f"{ERP}/app-purchase-order/create", json=body, headers=buyer_headers))
    row = query("SELECT id FROM erp_purchase_order WHERE deleted=0 AND commissioner_id=%s "
                "ORDER BY id DESC LIMIT 1", (BUYER_ID,))
    assert row, "下单后 DB 未查到采购订单"
    order_id = row[0]["id"]
    autotest_purchase_order_approve(api_session, auth_headers, order_id)
    print(f"[Fixture] purchase_order_id = {order_id}")
    yield order_id
    _cleanup(api_session, buyer_headers, "/purchase-order/delete", order_id)


def autotest_purchase_order_approve(api_session, auth_headers, autotest_purchase_order):
    """审批采购订单（admin 鉴权，PUT purchase-order/approve）"""
    body = {
        "id": autotest_purchase_order,
        "approved": True,
        "rejectReason": "autotest自动审核",
    }
    r = _assert_ok(api_session.put(f"{ADMIN_URL}/admin-api/erp/purchase-order/approve",
                                   json=body, headers=auth_headers))
    return r["data"]
@pytest.fixture
def autotest_purchase_in(api_session, buyer_headers, auth_headers, autotest_purchase_order, autotest_product):
    """自建采购入库（依赖采购订单 + 产品；先完成发货到待到厂）→ 返回 id → 删除"""
    order_id = autotest_purchase_order
    product_id = autotest_product
    # 完成发货：订单从已审核/待发货 → 待到厂（入库前置）
    purchase_order_complete_shipping(api_session, buyer_headers, order_id)
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
