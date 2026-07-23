import pytest
from config import ADMIN_URL


class TestPayTransferPage:
    """获得转账订单分页"""

    @pytest.mark.smoke
    def test_PayTransferPage(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/pay/transfer/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
