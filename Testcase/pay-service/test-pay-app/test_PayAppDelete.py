import pytest
from config import ADMIN_URL


class TestPayAppDelete:
    """删除支付应用信息"""

    @pytest.mark.smoke
    def test_PayAppDelete(self, api_session, auth_headers, autotest_app_id, ok):
        url = f"{ADMIN_URL}/admin-api/pay/app/delete"
        params = {"id": autotest_app_id}
        ok(api_session.delete(url, params=params, headers=auth_headers))
