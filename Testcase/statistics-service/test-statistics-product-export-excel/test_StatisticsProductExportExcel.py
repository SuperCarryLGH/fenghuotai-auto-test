import pytest
from config import ADMIN_URL


class TestStatisticsProductExportExcel:
    """导出获得商品统计明细 Excel（日期维度）"""

    @pytest.mark.smoke
    def test_StatisticsProductExportExcel(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/statistics/product/export-excel"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
