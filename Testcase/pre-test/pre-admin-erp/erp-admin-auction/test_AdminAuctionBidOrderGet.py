import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminAuctionBidOrderGet(api_session, auth_headers):
    """获得竞拍单详情"""
    resp = api_session.get(f"{ADMIN_URL}/admin-api/erp/auction-bid-order/get",
                           params={"id": 1}, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"竞拍单查询失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"] is not None, "竞拍单查询返回 data 为空"
    print(f"竞拍单信息:{data['data']}")
