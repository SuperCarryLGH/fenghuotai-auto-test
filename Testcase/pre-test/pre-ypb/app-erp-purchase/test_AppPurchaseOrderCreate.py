import pytest
from config import APP_URL


class TestAppPurchaseOrderCreate:
    """新增采购订单"""

    @pytest.mark.smoke
    def test_create(self, api_session, buyer_headers, ok, autotest_supplier, autotest_product, autotest_purchase_plan):
        supplier_id = autotest_supplier
        product_id = autotest_product
        plan_id = autotest_purchase_plan
        url = f"{APP_URL}/admin-api/erp/app-purchase-order/create"
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
            "commissionerId": 2090281734832517121,
            "commissionerName": "autotest采购员",
            "commissionerPhone": "18700000000",
        }
        r = ok(api_session.post(url, json=body, headers=buyer_headers))
        from Common.DB import query
        row = query("SELECT id FROM erp_purchase_order WHERE deleted=0 AND commissioner_id=%s "
                    "ORDER BY id DESC LIMIT 1", (2090281734832517121,))
        assert row, "下单后 DB 未查到采购订单"
        order_id = row[0]["id"]
        try:
            api_session.delete(
                f"{APP_URL}/admin-api/erp/purchase-order/delete",
                params={"id": order_id},
                headers=buyer_headers,
            )
            print(f"[cleanup] 创建测试产生的采购订单 id={order_id} 已删除")
        except Exception as e:
            print(f"[cleanup] 删除失败 id={order_id}: {e}")
