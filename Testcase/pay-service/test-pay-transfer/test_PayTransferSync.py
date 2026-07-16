import pytest
from config import APP_URL


class TestPayTransferSync:
    """同步转账单"""

    @pytest.mark.smoke
    def test_PayTransferSync(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/pay/transfer/sync"
        params = {
            # TODO: 补充查询参数
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
