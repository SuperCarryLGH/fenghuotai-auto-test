import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_admin_order

common = load_common()
module_data = load_recycle_admin_order()


class Test_AdminApiRecycleAdminOrderPage:
    """admin回收订单分页"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAdminOrderPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/admin-order/page"
        params = {
            "pageNo": common['common']['page']['pageNo'],
            "pageSize": common['common']['page']['pageSize'],
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
