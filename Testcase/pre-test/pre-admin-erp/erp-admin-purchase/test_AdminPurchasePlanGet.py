import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminPurchasePlanGet(api_session, auth_headers, autotest_purchase_plan):
    plan_id = autotest_purchase_plan
    resp = api_session.get(f"{ADMIN_URL}/admin-api/erp/purchase-plan/get",
                           params={"id": plan_id}, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"采购计划查询失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"]["id"] == plan_id, f"采购计划查询不匹配，期望：{plan_id}，实际：{data}"
    print(f"采购计划信息:{data['data']}")
