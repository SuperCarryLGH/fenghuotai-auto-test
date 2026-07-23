import pytest
from config import ADMIN_URL


class TestPayAppGet:
    """获得支付应用信息"""

    @pytest.mark.smoke
    def test_PayAppGet(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/pay/app/get"
        params = {
            "id" : 1
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
