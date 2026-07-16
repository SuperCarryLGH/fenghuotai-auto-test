import pytest
from config import ADMIN_URL


class TestPayAppDelete:
    """删除支付应用信息"""

    @pytest.mark.smoke
    def test_PayAppDelete(self, api_session, auth_headers, pay_app_id):
        url = f"{ADMIN_URL}/admin-api/pay/app/delete"
        params = {"id": pay_app_id}
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
