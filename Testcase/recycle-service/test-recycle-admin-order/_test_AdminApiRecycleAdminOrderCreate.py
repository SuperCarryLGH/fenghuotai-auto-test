import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_admin_order

common = load_common()
module_data = load_recycle_admin_order()


class Test_AdminApiRecycleAdminOrderCreate:
    """admin创建回收订单"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAdminOrderCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/admin-order/create"
        suffix = str(int(time.time()))
        body = {
            "name": f"{module_data['admin_order']['name']}_{suffix}",
            "status": common['common']['status']['enabled'],
        }
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
