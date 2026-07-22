import pytest
from config import ADMIN_URL


class TestErpStockInPage:
    """获得其它入库单分页"""

    @pytest.mark.smoke
    def test_ErpStockInPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/erp/stock-in/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)

 == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
