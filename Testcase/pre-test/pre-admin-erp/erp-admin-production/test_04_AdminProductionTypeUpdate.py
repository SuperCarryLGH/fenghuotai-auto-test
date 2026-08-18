import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminProductionType_update(api_session, auth_headers, production_type_create, production_product):
    """更新生产类型"""
    production_type_id = production_type_create
    product_id = production_product
    body = {
        "id": production_type_id,
        "name": "测试生产类型-更新",
        "status": 0,
        "remark": "autotest-update",
        "materialProductIds": [product_id],
        "productProductIds": [product_id],
    }
    resp = api_session.put(f"{ADMIN_URL}/admin-api/erp/production-type/update", json=body, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"生产类型更新失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"] is True, f"生产类型更新失败，编号：{production_type_id}"
    print(f"生产类型更新成功；{data['data']}")
