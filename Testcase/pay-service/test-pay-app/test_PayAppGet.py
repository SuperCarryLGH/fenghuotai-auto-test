import pytest
from config import ADMIN_URL


class TestPayAppGet:
    """获得支付应用信息"""

    @pytest.mark.smoke
    def test_PayAppGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/app/get"
        params = {
            "id" : 1
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
