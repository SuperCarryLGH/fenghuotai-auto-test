import pytest
from config import ADMIN_URL


class TestStatisticsTradeExportExcel:
    """导出获得交易状况明细 Excel"""

    @pytest.mark.smoke
    def test_StatisticsTradeExportExcel(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/statistics/trade/export-excel"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200 and len(resp.content) > 0
        print(f"下载成功, 文件大小={len(resp.content)}bytes")
