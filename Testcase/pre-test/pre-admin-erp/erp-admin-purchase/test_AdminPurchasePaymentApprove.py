import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminPurchasePaymentApprove(api_session, auth_headers, autotest_purchase_in):
    payment_id = autotest_purchase_in
    resp = api_session.put(f"{ADMIN_URL}/admin-api/erp/purchase-payment/approve",
                           params={"id": payment_id}, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"付款单审批失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"] is True, f"付款单审批失败，编号：{payment_id}"
    print(f"付款单审批成功；{data['data']}")
