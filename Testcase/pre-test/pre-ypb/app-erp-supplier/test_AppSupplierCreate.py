import pytest
from config import APP_URL

@pytest.mark.smoke
def test_AppSupplierCreate(api_session, auth_headers):
    body = {"id": 0, "name": "测试供应商", "legalName": "测试企业", "contact": "芋艿", "mobile": "15601691300", "status": 1, "sort": 10, "taxNo": "91130803MA098BY05W", "idCard": "110101199001011234", "supplierType": 10}
    resp = api_session.post(f"{APP_URL}/admin-api/erp/app-supplier/create", json=body, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"接口调用失败: code={data.get('code')}, msg={data.get('msg')}"
    print(f"调用成功，响应：{data}")
