import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminProductionType_page(api_session, auth_headers, production_type_create):
    """获得生产类型分页"""
    production_type_id = production_type_create
    params = {
        "pageNo": 1,
        "pageSize": 10,
        "id": production_type_id,
    }
    resp = api_session.get(f"{ADMIN_URL}/admin-api/erp/production-type/page", params=params, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"生产类型分页查询失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"]["total"] >= 1, "生产类型列表信息缺失！"
    ids = [item["id"] for item in data["data"]["list"]]
    assert production_type_id in ids, f"分页结果中未包含创建的生产类型：{production_type_id}"
    print(f"生产类型列表分页数据：{data['data']}")
