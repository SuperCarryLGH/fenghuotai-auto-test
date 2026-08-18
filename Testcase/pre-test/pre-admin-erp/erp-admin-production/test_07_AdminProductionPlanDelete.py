import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminProductionPlan_Delete(api_session, auth_headers, production_plan_create):
    """删除生产计划"""
    production_plan_id = production_plan_create
    resp = api_session.delete(f"{ADMIN_URL}/admin-api/erp/production-plan/delete",
                              params={"id": production_plan_id}, headers=auth_headers)
    assert resp.status_code == 200
    assert resp.json()["data"] is True, f"生产计划删除失败，生产计划编号：{production_plan_id}"
    print("生产计划删除成功，生产计划编号：%s" % production_plan_id)
