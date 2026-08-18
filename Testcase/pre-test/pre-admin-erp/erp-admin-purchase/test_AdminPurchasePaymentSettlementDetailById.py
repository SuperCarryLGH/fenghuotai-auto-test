import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminPurchasePaymentSettlementDetailById(api_session, auth_headers, autotest_purchase_in):
    """根据付款单ID获取结算详情"""
    payment_id = autotest_purchase_in
    resp = api_session.get(f"{ADMIN_URL}/admin-api/erp/purchase-payment/settlement-detail-by-id",
                           params={"id": payment_id}, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"按付款单查询结算详情失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"] is not None, "按付款单查询结算详情返回 data 为空"
    print(f"付款单结算详情:{data['data']}")
