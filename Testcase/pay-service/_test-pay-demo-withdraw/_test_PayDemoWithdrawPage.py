import pytest
from config import ADMIN_URL


class TestPayDemoWithdrawPage:
    """获得示例提现单分页"""

    @pytest.mark.smoke
    def test_PayDemoWithdrawPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/demo-withdraw/page"
        params = {"pageNo": 1, "pageSize": 10}
        resp = api_session.get(url, params=params, headers=auth_headers)
