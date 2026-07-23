import pytest
from config import ADMIN_URL


class TestOrderGetDetail:
    """获得交易订单详情"""

    @pytest.mark.smoke
    def test_OrderGetDetail(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/trade/order/get-detail"
        params = {"id": 1}  # TODO: 补充查询参数
        ok(api_session.get(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
