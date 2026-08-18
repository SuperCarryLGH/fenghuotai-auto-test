import pytest
from config import APP_URL

@pytest.mark.smoke
def test_AppProductionTaskScanPrepare(api_session, auth_headers, app_production_task):
    """扫码备货"""
    data_id = app_production_task
    body = {"taskId": data_id, "packageCode": "PKG20260101001", "weight": 50, "stockLocationId": 100, "stockLocationName": "A区-01", "price": 100}
    resp = api_session.post(f"{APP_URL}/admin-api/erp/app-production-task/scan-prepare", json=body, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"接口调用失败: code={data.get('code')}, msg={data.get('msg')}"
    print(f"调用成功，响应：{data}")
