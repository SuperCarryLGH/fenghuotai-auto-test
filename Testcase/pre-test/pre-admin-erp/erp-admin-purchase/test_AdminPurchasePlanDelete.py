import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminPurchasePlanDelete(api_session, auth_headers, autotest_purchase_plan):
    plan_id = autotest_purchase_plan
    resp = api_session.delete(f"{ADMIN_URL}/admin-api/erp/purchase-plan/delete",
                              params={"id": plan_id}, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"采购计划删除失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"] is True, f"采购计划删除失败，编号：{plan_id}"
    print(f"采购计划删除成功，编号：{plan_id}")
