import pytest
from config import ADMIN_URL


@pytest.mark.smoke
def test_AdminAuctionRoundUpdateStatus(api_session, auth_headers, autotest_auction_round):
    round_id = autotest_auction_round
    body = {
        "id": round_id,
        "status": 2,
    }
    resp = api_session.put(f"{ADMIN_URL}/admin-api/erp/auction-round/update-status", json=body, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0, f"竞拍场次上架/下架失败: code={data.get('code')}, msg={data.get('msg')}"
    assert data["data"] is True, "竞拍场次上架/下架失败"
    print(f"竞拍场次上架/下架成功；{data['data']}")
