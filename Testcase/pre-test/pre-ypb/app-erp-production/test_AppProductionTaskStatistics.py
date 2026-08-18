import pytest
from config import APP_URL

@pytest.mark.smoke
def test_AppProductionTaskStatistics(api_session, auth_headers, app_production_plan):
    data_id = app_production_plan
    params = {"planId": data_id}
    resp = api_session.get(f"{APP_URL}/admin-api/erp/app-production-task/statistics", params=params, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"接口调用失败: code={data.get('code')}, msg={data.get('msg')}"
    print(f"调用成功，响应：{data}")
