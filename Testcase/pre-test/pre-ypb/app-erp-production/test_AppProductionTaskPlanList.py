import pytest
from config import APP_URL

@pytest.mark.smoke
def test_AppProductionTaskPlanList(api_session, auth_headers):
    """获得最近三个月的生产计划列表"""
    resp = api_session.get(f"{APP_URL}/admin-api/erp/app-production-task/plan-list", headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"接口调用失败: code={data.get('code')}, msg={data.get('msg')}"
    print(f"调用成功，响应：{data}")
