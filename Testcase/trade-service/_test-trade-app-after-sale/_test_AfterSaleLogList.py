import pytest
from config import APP_URL


class TestAfterSaleLogList:
    """获得售后日志列表"""

    @pytest.mark.smoke
    def test_AfterSaleLogList(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/trade/after-sale-log/list"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
