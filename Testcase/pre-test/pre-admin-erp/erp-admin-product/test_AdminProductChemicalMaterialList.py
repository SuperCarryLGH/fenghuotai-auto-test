import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminProductChemicalMaterialList(api_session, auth_headers):
    """获得指定分类下开启的产品列表"""
    params = {
        "categoryId": 2079825943876988929,
    }
    resp = api_session.get(f"{ADMIN_URL}/admin-api/erp/product/chemical-material-list",
                           params=params, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"化学原材料产品列表查询失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"] is not None, "化学原材料产品列表返回 data 为空"
    print(f"化学原材料产品列表：{data['data']}")
