import pytest
from config import APP_URL

@pytest.mark.smoke
def test_AppProductionTaskMaterialStock(api_session, auth_headers, app_production_task):
    """获得生产任务备货物资列表（产品+仓库库存联动）"""
    data_id = app_production_task
    params = {"taskId": data_id}
    resp = api_session.get(f"{APP_URL}/admin-api/erp/app-production-task/material-stock", params=params, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"接口调用失败: code={data.get('code')}, msg={data.get('msg')}"
    print(f"调用成功，响应：{data}")
