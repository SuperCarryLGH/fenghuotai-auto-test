import pytest
from config import APP_URL
from Common.loader import load_common
from Common.loader import load_recycle_clear_order_driver

common = load_common()
driver_data = load_recycle_clear_order_driver()


class Test_AppApiRecycleClearOrderDriverDepart:
    """司机出发"""

    @pytest.mark.smoke
    def test_AppApiRecycleClearOrderDriverDepart(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/recycle/clear/order/driver/depart"
        body = {"id": driver_data['driver']['order_id']}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
