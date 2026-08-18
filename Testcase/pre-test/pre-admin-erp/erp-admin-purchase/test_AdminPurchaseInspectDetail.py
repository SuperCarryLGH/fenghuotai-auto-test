import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminPurchaseInspectDetail(api_session, auth_headers, autotest_purchase_order):
    """获取采购质检详情"""
    order_id = autotest_purchase_order
    resp = api_session.get(f"{ADMIN_URL}/admin-api/erp/purchase-inspect/detail",
                           params={"id": order_id}, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"采购质检详情查询失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"]["id"] == order_id, f"采购质检详情不匹配，期望：{order_id}，实际：{data}"
    print(f"采购质检详情:{data['data']}")
