import pytest
from config import ADMIN_URL


class TestPayRefundPage:
    """获得退款订单分页"""

    @pytest.mark.smoke
    def test_PayRefundPage(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/pay/refund/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
