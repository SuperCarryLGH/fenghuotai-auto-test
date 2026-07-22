import pytest
from config import ADMIN_URL
from Common.loader import load_common
from Common.loader import load_recycle_clear_order_weigher

common = load_common()
weigher_data = load_recycle_clear_order_weigher()


class Test_AdminApiRecycleClearOrderWeigherGetArrivedDriver:
    """称重员获取已到达司机"""

    @pytest.mark.smoke
    def test_AdminApiRecycleClearOrderWeigherGetArrivedDriver(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/clear-order/weigher/get-arrived-driver"
        params = {"id": weigher_data['weigher']['order_id']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
