import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminAuctionBidOrderPage(api_session, auth_headers):
    params = {
        "pageNo": 1,
        "pageSize": 10,
    }
    resp = api_session.get(f"{ADMIN_URL}/admin-api/erp/auction-bid-order/page", params=params, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"竞拍单分页查询失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"]["total"] >= 0, "竞拍单列表信息缺失！"
    print(f"竞拍单列表分页数据：{data['data']}")
