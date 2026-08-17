import pytest
from config import ADMIN_URL


class TestAppPurchaseOrderCreate:
    """新增采购订单"""

    @pytest.mark.smoke
    def test_create(self, api_session, auth_headers, ok, autotest_supplier, autotest_product, autotest_purchase_plan):
        supplier_id = autotest_supplier
        product_id = autotest_product
        plan_id = autotest_purchase_plan
        url = f"{ADMIN_URL}/admin-api/erp/app-purchase-order/create"
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
        r = ok(api_session.post(url, json=body, headers=auth_headers))
        order_id = r["data"]
        try:
            api_session.delete(
                f"{ADMIN_URL}/admin-api/erp/purchase-order/delete",
                params={"id": order_id},
                headers=auth_headers,
            )
            print(f"[cleanup] 创建测试产生的采购订单 id={order_id} 已删除")
        except Exception as e:
            print(f"[cleanup] 删除失败 id={order_id}: {e}")
