import pytest
from config import ADMIN_URL


class TestOrderGetExpressTrackList:
    """获得交易订单的物流轨迹"""

    @pytest.mark.smoke
    def test_OrderGetExpressTrackList(self, api_session, auth_headers, order_id):
        url = f"{ADMIN_URL}/admin-api/trade/order/get-express-track-list"
        params = {"id": order_id}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
