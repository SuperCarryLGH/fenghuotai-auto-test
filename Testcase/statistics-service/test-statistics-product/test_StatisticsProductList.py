import pytest
from config import ADMIN_URL


class TestStatisticsProductList:
    """获得商品统计明细（日期维度）"""

    @pytest.mark.smoke
    def test_StatisticsProductList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/statistics/product/list"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
