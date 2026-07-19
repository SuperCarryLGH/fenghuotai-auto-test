import pytest
from config import ADMIN_URL


class TestPayDemoOrderPage:
    """获得示例订单分页"""

    @pytest.mark.smoke
    def test_PayDemoOrderPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/demo-order/page"
        params = {"pageNo": 1, "pageSize": 10}
        resp = api_session.get(url, params=params, headers=auth_headers)
