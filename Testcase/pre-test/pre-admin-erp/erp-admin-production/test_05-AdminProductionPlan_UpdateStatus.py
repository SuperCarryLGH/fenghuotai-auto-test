import pytest
from config import ADMIN_URL
@pytest.mark.smoke
def test_AdminProductionPlan_UpdateStatus(api_session,auth_headers,production_plan_create):
    production_plan_id = production_plan_create
    data = {
        "id":production_plan_id,
        "status":20,
        "rejectReason":"测试测试预算不足"
    }
    resp = api_session.put(f"{ADMIN_URL}/admin-api/erp/production-plan/update-status",json=data,headers=auth_headers)
    assert resp.status_code == 200
    date = resp.json()
    assert date["data"] is True,f"生产计划状态变更失败:{production_plan_id}"
    print("生产计划变更成功：%s,"%date["data"])