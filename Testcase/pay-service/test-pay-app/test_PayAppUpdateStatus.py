import pytest
from config import ADMIN_URL


class TestPayAppUpdateStatus:
    """更新支付应用状态"""

    @pytest.mark.smoke
    def test_PayAppUpdateStatus(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/app/update-status"
        body = {
              "id": 2077228704176402434,
              "status": 1
            }
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
