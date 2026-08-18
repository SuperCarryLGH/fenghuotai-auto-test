import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminAuctionRoundItemGet(api_session, auth_headers, autotest_auction_round_item):
    """获得竞拍商品详情"""
    item_id = autotest_auction_round_item
    resp = api_session.get(f"{ADMIN_URL}/admin-api/erp/auction-round/item-get",
                           params={"id": item_id}, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"竞拍商品查询失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"] is not None, "竞拍商品查询返回 data 为空"
    print(f"竞拍商品信息:{data['data']}")
