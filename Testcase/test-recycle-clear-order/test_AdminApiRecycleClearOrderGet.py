import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_clear_order

common = load_common()
module_data = load_recycle_clear_order()


class Test_AdminApiRecycleClearOrderGet:
    """admin获取回收清运单详情"""

    @pytest.mark.smoke
    def test_AdminApiRecycleClearOrderGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/clear-order/get"
        params = {"id": common['common']['id']['valid']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
