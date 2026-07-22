import pytest
from config import ADMIN_URL


class TestErpStockInWeightStat:
    """统计入库重量总和"""

    @pytest.mark.smoke
    def test_ErpStockInWeightStat(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/erp/stock-in/weight-stat"
        body = {
            # TODO: 补充请求体参数
        }
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)

 == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
