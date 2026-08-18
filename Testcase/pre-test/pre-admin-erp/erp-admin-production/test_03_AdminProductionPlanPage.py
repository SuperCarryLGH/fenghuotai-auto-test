
import pytest
from config import ADMIN_URL
@pytest.mark.smoke
def test_AdminProductionPlan_page(api_session,auth_headers):
    body = {
        "pageNo":1,
        "pageSize":10,
    }
    resp = api_session.get(f"{ADMIN_URL}/admin-api/erp/production-plan/page",params=body,headers=auth_headers)
    assert resp.status_code == 200
    date = resp.json()
    assert date["data"]["total"] >= 1,f"生产计划列表信息缺失！"
    print("生产计划列表分页数据：%s"%date["data"])
