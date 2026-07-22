import pytest
from config import ADMIN_URL


class TestErpSaleStatisticsTimeSummary:
    """获得销售时间段统计"""

    @pytest.mark.smoke
    def test_ErpSaleStatisticsTimeSummary(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/erp/sale-statistics/time-summary"
        params = {
            # TODO: 补充查询参数
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
