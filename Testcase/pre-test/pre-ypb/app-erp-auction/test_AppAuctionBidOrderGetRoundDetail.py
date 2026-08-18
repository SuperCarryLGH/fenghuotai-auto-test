import pytest
from config import APP_URL

@pytest.mark.smoke
def test_AppAuctionBidOrderGetRoundDetail(api_session, auth_headers, app_auction_round):
    """获得竞拍场次详情（竞拍中状态）:根据竞拍场次ID查询竞拍中的商品列表，包含每个商品的总出价次数和当前用户的最新出价"""
    data_id = app_auction_round
    params = {"roundId": data_id}
    resp = api_session.get(f"{APP_URL}/admin-api/erp/app-auction-bid-order/get-round-detail", params=params, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"接口调用失败: code={data.get('code')}, msg={data.get('msg')}"
    print(f"调用成功，响应：{data}")
