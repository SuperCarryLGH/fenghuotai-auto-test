import pytest
from config import APP_URL

@pytest.mark.smoke
def test_AppProductionTaskCancelTask(api_session, auth_headers, app_production_task):
    """取消任务"""
    data_id = app_production_task
    body = {"taskId": data_id, "cancelReason": "原料不足"}
    resp = api_session.post(f"{APP_URL}/admin-api/erp/app-production-task/cancel-task", json=body, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"接口调用失败: code={data.get('code')}, msg={data.get('msg')}"
    print(f"调用成功，响应：{data}")
