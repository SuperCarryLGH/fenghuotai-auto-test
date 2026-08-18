import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminAuctionRoundDelete(api_session, auth_headers, autotest_auction_round):
    """删除竞拍场次"""
    round_id = autotest_auction_round
    resp = api_session.delete(f"{ADMIN_URL}/admin-api/erp/auction-round/delete",
                              params={"ids": [round_id]}, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"竞拍场次删除失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"] is True, "竞拍场次删除失败"
    print(f"竞拍场次删除成功；{data['data']}")
