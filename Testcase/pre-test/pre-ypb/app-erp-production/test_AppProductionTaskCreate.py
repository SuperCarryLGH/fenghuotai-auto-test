import pytest
from config import APP_URL

@pytest.mark.smoke
def test_AppProductionTaskCreate(api_session, auth_headers, app_production_plan):
    """新增生产任务"""
    data_id = app_production_plan
    body = {"planId": data_id, "workerCount": 5, "remark": "autotest", "taskStartTime": "2026-01-01 08:00:00", "taskEndTime": "2026-01-01 18:00:00"}
    resp = api_session.post(f"{APP_URL}/admin-api/erp/app-production-task/create", json=body, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"接口调用失败: code={data.get('code')}, msg={data.get('msg')}"
    print(f"调用成功，响应：{data}")
