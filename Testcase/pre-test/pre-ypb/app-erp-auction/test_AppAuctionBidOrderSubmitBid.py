import pytest
from config import APP_URL

@pytest.mark.smoke
def test_AppAuctionBidOrderSubmitBid(api_session, auth_headers, app_auction_round_item):
    """提交竞拍商品出价:维护竞拍单、出价记录"""
    data_id = app_auction_round_item
    body = {"itemId": data_id, "bidPrice": 191, "bidQuantity": 10}
    resp = api_session.post(f"{APP_URL}/admin-api/erp/app-auction-bid-order/submit-bid", json=body, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"接口调用失败: code={data.get('code')}, msg={data.get('msg')}"
    print(f"调用成功，响应：{data}")
