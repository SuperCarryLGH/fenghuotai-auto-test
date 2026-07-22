import pytest
from config import ADMIN_URL


class TestOrderGetDetail:
    """获得交易订单详情"""

    @pytest.mark.smoke
    def test_OrderGetDetail(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/trade/order/get-detail"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
