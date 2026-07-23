import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_admin_order

common = load_common()
module_data = load_recycle_admin_order()


class Test_AdminApiRecycleAdminOrderUpdateStatus:
    """admin更新回收订单状态"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAdminOrderUpdateStatus(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/admin-order/update-status"
        body = {"id": module_data['admin_order']['id'], "status": common['common']['status']['enabled']}
        ok(api_session.put(url, json=body, headers=auth_headers))
