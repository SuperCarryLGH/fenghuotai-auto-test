import pytest
from config import APP_URL

@pytest.mark.smoke
def test_AppProductionTaskProductStockIn(api_session, auth_headers, app_production_task, app_product):
    data_id = app_production_task
    body = {"taskId": data_id, "productId": app_product, "weight": 100, "packageCount": 2, "stockLocationId": 200, "stockLocationName": "B区-01", "remark": "合格"}
    resp = api_session.post(f"{APP_URL}/admin-api/erp/app-production-task/product-stock-in", json=body, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"接口调用失败: code={data.get('code')}, msg={data.get('msg')}"
    print(f"调用成功，响应：{data}")
