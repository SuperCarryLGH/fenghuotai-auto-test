import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminAuctionRoundItemDelete(api_session, auth_headers, autotest_auction_round_item):
    """删除竞拍商品"""
    item_id = autotest_auction_round_item
    resp = api_session.delete(f"{ADMIN_URL}/admin-api/erp/auction-round/item-delete",
                              params={"id": item_id}, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"竞拍商品删除失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"] is True, "竞拍商品删除失败"
    print(f"竞拍商品删除成功；{data['data']}")
