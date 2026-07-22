import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_admin_order

common = load_common()
module_data = load_recycle_admin_order()


class Test_AdminApiRecycleAdminOrderGet:
    """admin获取回收订单详情"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAdminOrderGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/admin-order/get"
        params = {"id": common['common']['id']['valid']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        print(resp.json())