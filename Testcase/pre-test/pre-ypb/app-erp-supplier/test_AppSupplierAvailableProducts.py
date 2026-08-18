import pytest
from config import APP_URL

@pytest.mark.smoke
def test_AppSupplierAvailableProducts(api_session, auth_headers, app_supplier):
    """获取供应商可以提供的产品信息（仅 id 与 name，仅启用）"""
    data_id = app_supplier
    params = {"id": data_id}
    resp = api_session.get(f"{APP_URL}/admin-api/erp/app-supplier/available-products", params=params, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"接口调用失败: code={data.get('code')}, msg={data.get('msg')}"
    print(f"调用成功，响应：{data}")
