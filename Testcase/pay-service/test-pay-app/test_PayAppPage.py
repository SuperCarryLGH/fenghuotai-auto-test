import pytest
from config import ADMIN_URL


class TestPayAppPage:
    """获得支付应用信息分页"""

    @pytest.mark.smoke
    def test_PayAppPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/app/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
