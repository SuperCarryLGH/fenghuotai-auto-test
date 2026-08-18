import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminPurchasePaymentSettlementDetail(api_session, auth_headers, autotest_supplier, autotest_purchase_order):
    supplier_id = autotest_supplier
    order_id = autotest_purchase_order
    params = {
        "supplierId": supplier_id,
        "purchaseOrderIds": [order_id],
    }
    resp = api_session.get(f"{ADMIN_URL}/admin-api/erp/purchase-payment/settlement-detail",
                           params=params, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"发起结算详情查询失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"] is not None, "发起结算详情返回 data 为空"
    print(f"发起结算详情:{data['data']}")
