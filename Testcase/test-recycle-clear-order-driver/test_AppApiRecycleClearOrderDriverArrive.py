import pytest
from config import APP_URL
from Common.loader import load_common
from Common.loader import load_recycle_clear_order_driver

common = load_common()
driver_data = load_recycle_clear_order_driver()


class Test_AppApiRecycleClearOrderDriverArrive:
    """司机到达"""

    @pytest.mark.smoke
    def test_AppApiRecycleClearOrderDriverArrive(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/recycle/clear/order/driver/arrive"
        body = {"id": driver_data['driver']['order_id']}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
