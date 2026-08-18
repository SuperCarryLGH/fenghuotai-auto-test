import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminProductionType_get(api_session, auth_headers, production_type_create):
    production_type_id = production_type_create
    resp = api_session.get(f"{ADMIN_URL}/admin-api/erp/production-type/get",
                           params={"id": production_type_id}, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"生产类型查询失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"]["id"] == production_type_id, f"生产类型查询不匹配，期望：{production_type_id}，实际：{data}"
    print(f"生产类型信息:{data['data']}")
