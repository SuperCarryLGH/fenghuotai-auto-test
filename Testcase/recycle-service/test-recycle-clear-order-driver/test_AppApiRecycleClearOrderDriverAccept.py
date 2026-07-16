import pytest
from config import APP_URL
from Common.loader import load_recycle_clear_order_driver

driver_data = load_recycle_clear_order_driver()


class Test_AppApiRecycleClearOrderDriverAccept:
    """司机接单"""

    @pytest.mark.smoke
    def test_AppApiRecycleClearOrderDriverAccept(self, api_session, login_tool):
        url = f"{APP_URL}/app-api/recycle/clear/order/driver/accept"
        mobile = driver_data['driver']['mobile']
        headers = {"Authorization": f"Bearer {login_tool.app_login_with(mobile)}"}
        body = {"id": driver_data['driver']['order_id']}
        resp = api_session.post(url, json=body, headers=headers)
        assert resp.status_code == 200
