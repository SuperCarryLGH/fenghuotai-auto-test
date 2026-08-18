import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminProductionType_Delete(api_session, auth_headers, production_type_create):
    production_type_id = production_type_create
    resp = api_session.delete(f"{ADMIN_URL}/admin-api/erp/production-type/delete",
                              params={"id": production_type_id}, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"生产类型删除失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"] is True, f"生产类型删除失败，编号：{production_type_id}"
    print(f"生产类型删除成功，编号：{production_type_id}")
