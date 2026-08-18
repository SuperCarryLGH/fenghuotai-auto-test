import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminPurchasePlanApprove(api_session, auth_headers, autotest_purchase_plan):
    """审批采购计划"""
    plan_id = autotest_purchase_plan
    body = {
        "id": plan_id,
        "approved": True,
        "rejectReason": "",
    }
    resp = api_session.put(f"{ADMIN_URL}/admin-api/erp/purchase-plan/approve", json=body, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"采购计划审批失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"] is True, f"采购计划审批失败，编号：{plan_id}"
    print(f"采购计划审批成功；{data['data']}")
