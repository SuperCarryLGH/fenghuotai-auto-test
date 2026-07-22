import pytest
from config import ADMIN_URL


class TestErpStockOutPage:
    """获得其它出库单分页"""

    @pytest.mark.smoke
    def test_ErpStockOutPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/erp/stock-out/page"
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
