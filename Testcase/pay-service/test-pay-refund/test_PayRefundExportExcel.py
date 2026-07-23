import pytest
from config import ADMIN_URL


class TestPayRefundExportExcel:
    """导出退款订单 Excel"""

    @pytest.mark.smoke
    def test_PayRefundExportExcel(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/pay/refund/export-excel"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
        print(f"下载成功, 文件大小={len(resp.content)}bytes")
