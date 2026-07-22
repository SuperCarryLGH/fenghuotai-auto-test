import pytest
from config import ADMIN_URL


class TestErpPurchaseStatisticsTimeSummary:
    """获得采购时间段统计"""

    @pytest.mark.smoke
    def test_ErpPurchaseStatisticsTimeSummary(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/erp/purchase-statistics/time-summary"
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
