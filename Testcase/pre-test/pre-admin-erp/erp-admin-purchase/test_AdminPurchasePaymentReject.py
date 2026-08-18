import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminPurchasePaymentReject(api_session, auth_headers, autotest_purchase_in):
    payment_id = autotest_purchase_in
    params = {
        "id": payment_id,
        "rejectReason": "信息不完整",
    }
    resp = api_session.put(f"{ADMIN_URL}/admin-api/erp/purchase-payment/reject",
                           params=params, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"付款单驳回失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"] is True, f"付款单驳回失败，编号：{payment_id}"
    print(f"付款单驳回成功；{data['data']}")
