import pytest
from config import APP_URL


class TestConfigGet:
    """获得交易配置"""

    @pytest.mark.smoke
    def test_ConfigGet(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/trade/config/get"
        params = {"id": "trade_app_brokerage_id"}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
