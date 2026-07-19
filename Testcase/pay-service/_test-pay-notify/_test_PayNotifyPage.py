import pytest
from config import ADMIN_URL


class TestPayNotifyPage:
    """获得回调通知分页"""

    @pytest.mark.smoke
    def test_PayNotifyPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/notify/page"
        params = {"pageNo": 1, "pageSize": 10}
        resp = api_session.get(url, params=params, headers=auth_headers)
