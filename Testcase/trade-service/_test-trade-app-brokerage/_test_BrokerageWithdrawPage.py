import pytest
from config import APP_URL


class TestBrokerageWithdrawPage:
    """获得分销提现分页"""

    @pytest.mark.smoke
    def test_BrokerageWithdrawPage(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/trade/brokerage-withdraw/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
