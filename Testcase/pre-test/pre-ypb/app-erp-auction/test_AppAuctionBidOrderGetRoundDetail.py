import pytest
from config import APP_URL

@pytest.mark.smoke
def test_AppAuctionBidOrderGetRoundDetail(api_session, auth_headers, app_auction_round):
    data_id = app_auction_round
    params = {"roundId": data_id}
    resp = api_session.get(f"{APP_URL}/admin-api/erp/app-auction-bid-order/get-round-detail", params=params, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"接口调用失败: code={data.get('code')}, msg={data.get('msg')}"
    print(f"调用成功，响应：{data}")
