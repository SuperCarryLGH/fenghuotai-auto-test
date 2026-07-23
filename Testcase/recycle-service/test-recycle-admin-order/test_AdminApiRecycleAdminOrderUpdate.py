import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiRecycleAdminOrderUpdate:
    """admin更新回收订单"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAdminOrderUpdate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/admin-order/update"
        body = {
            "id": common['common']['id']['valid'],
            "orderNo": common['common']['id']['orderNo'],
            "clearStatus": common['common']['id']['clearStatus'],
            "addressId": common['common']['id']['addressId']
        }
        ok(api_session.put(url, json=body, headers=auth_headers))
