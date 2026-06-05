import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_admin_order

common = load_common()
module_data = load_recycle_admin_order()


class Test_AdminApiRecycleAdminOrderUpdate:
    """admin更新回收订单"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAdminOrderUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/admin-order/update"
        suffix = str(int(time.time()))
        body = {
            "id": common['common']['id']['valid'],
            "name": f"{module_data['admin_order']['update_name']}_{suffix}",
            "status": common['common']['status']['enabled'],
        }
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
