import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminAuctionRoundGet(api_session, auth_headers, autotest_auction_round):
    """获得竞拍场次详情"""
    round_id = autotest_auction_round
    resp = api_session.get(f"{ADMIN_URL}/admin-api/erp/auction-round/get",
                           params={"id": round_id}, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"竞拍场次查询失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"] is not None, "竞拍场次查询返回 data 为空"
    print(f"竞拍场次信息:{data['data']}")
