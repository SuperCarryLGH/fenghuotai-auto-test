import pytest
import time
from config import ADMIN_URL
@pytest.mark.smoke
def test_AdminProductionPlan_update(api_session,auth_headers,production_plan_create):
    """更新生产计划"""
    production_plan_id = production_plan_create
    body = {
        "id":production_plan_id,
        "title":"测试生产计划",
        "planEndDate":time.strftime("%Y-%m-%d",time.localtime()),
        "productionTypeId":1024,
        "targetQuantity":1000,
        "productIds":[1024]
    }
    resp = api_session.put(f"{ADMIN_URL}/admin-api/erp/production-plan/update",json=body,headers=auth_headers)
    assert resp.status_code == 200
    date = resp.json()
    assert date['data'] is True,f"生产计划更新失败，生产编号为：{production_plan_id}"
    print("生产计划更新成功；%s"%date['data'])