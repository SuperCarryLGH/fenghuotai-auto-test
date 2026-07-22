import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_admin_order

common = load_common()
module_data = load_recycle_admin_order()


class Test_AdminApiRecycleAdminOrderDelete:
    """admin删除回收订单"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAdminOrderDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/admin-order/delete"
        params = {"id": common['common']['id']['invalid']}
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        print(resp.json())