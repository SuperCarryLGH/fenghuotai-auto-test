import pytest
import time
from config import APP_URL
from Common.loader import load_common
from Common.loader import load_recycle_clear_order_driver
from Common.login import Login

common = load_common()
driver_data = load_recycle_clear_order_driver()


class Test_AppApiRecycleClearOrderDriverUpdateWeight:
    """司机更新重量"""

    @pytest.mark.smoke
    def test_AppApiRecycleClearOrderDriverUpdateWeight(self, api_session, login_tool):
        url = f"{APP_URL}/app-api/recycle/clear/order/driver/update-weight"
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        body = {"id": driver_data['driver']['order_id']}
        resp = api_session.post(url, json=body, headers=headers)
        assert resp.status_code == 200
