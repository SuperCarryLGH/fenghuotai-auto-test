import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminProductionPlan_get(api_session,auth_headers,production_plan_create):
    """获得生产计划"""
    production_plan_id = production_plan_create
    params = {"id": production_plan_id}
    resp = api_session.get(f"{ADMIN_URL}/admin-api/erp/production-plan/get",params=params,headers=auth_headers)
    assert resp.status_code == 200
    date = resp.json()
    assert int(date["data"]["id"]) == production_plan_id,f"生产计划查询不匹配-查询编号：{production_plan_id},查询的编号：{date}"
    print("生产计划信息:%s"%date["data"]["id"])