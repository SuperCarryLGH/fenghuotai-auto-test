import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_clear_order_weigher

common = load_common()
weigher_data = load_recycle_clear_order_weigher()


class Test_AdminApiRecycleClearOrderWeigherDashboard:
    """称重员仪表盘"""

    @pytest.mark.smoke
    def test_AdminApiRecycleClearOrderWeigherDashboard(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/clear-order/weigher/dashboard"
        resp = api_session.get(url, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
