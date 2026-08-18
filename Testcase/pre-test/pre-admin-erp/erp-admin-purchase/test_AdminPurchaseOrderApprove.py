import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminPurchaseOrderApprove(api_session, auth_headers, autotest_purchase_order):
    """审批采购订单"""
    order_id = autotest_purchase_order
    body = {
        "id": order_id,
        "approved": True,
        "rejectReason": "",
    }
    resp = api_session.put(f"{ADMIN_URL}/admin-api/erp/purchase-order/approve", json=body, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"采购订单审批失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"] is True, f"采购订单审批失败，编号：{order_id}"
    print(f"采购订单审批成功；{data['data']}")
