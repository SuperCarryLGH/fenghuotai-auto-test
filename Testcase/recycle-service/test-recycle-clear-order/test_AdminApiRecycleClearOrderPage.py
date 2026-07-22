import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_clear_order

common = load_common()
module_data = load_recycle_clear_order()


class Test_AdminApiRecycleClearOrderPage:
    """admin回收清运单分页"""

    @pytest.mark.smoke
    def test_AdminApiRecycleClearOrderPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/clear-order/page"
        params = {
            "pageNo": common['common']['page']['pageNo'],
            "pageSize": common['common']['page']['pageSize'],
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
