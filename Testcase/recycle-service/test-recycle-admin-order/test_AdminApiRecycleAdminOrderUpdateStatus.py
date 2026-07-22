import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiRecycleAdminOrderUpdateStatus:
    """admin更新回收订单状态"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAdminOrderUpdateStatus(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/admin-order/update-status"
        body = {"id": common['common']['id']['valid'], "status": common['common']['status']['enabled']}
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        print(resp.json())
