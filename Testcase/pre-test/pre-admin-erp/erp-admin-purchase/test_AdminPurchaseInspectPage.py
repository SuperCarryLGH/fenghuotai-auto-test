import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminPurchaseInspectPage(api_session, auth_headers):
    params = {
        "inspectType": 0,
        "pageNo": 1,
        "pageSize": 10,
    }
    resp = api_session.get(f"{ADMIN_URL}/admin-api/erp/purchase-inspect/page", params=params, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"采购质检列表查询失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"]["total"] >= 0, "采购质检列表信息缺失！"
    print(f"采购质检列表分页数据：{data['data']}")
