import pytest
from config import APP_URL

@pytest.mark.smoke
def test_AppAuctionBidOrderGetItemBidDetail(api_session, auth_headers, app_auction_round_item):
    """获得竞拍商品出价详情:根据商品ID查询商品基本信息、总出价次数、当前用户的出价情况，包含是否已出价标识"""
    data_id = app_auction_round_item
    params = {"itemId": data_id}
    resp = api_session.get(f"{APP_URL}/admin-api/erp/app-auction-bid-order/get-item-bid-detail", params=params, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"接口调用失败: code={data.get('code')}, msg={data.get('msg')}"
    print(f"调用成功，响应：{data}")
