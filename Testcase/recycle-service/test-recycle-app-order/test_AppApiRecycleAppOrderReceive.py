import pytest
import time
from config import APP_URL
from Common.loader import load_common
from Common.loader import load_recycle_app_order
from Common.login import Login

common = load_common()
order_data = load_recycle_app_order()


class Test_AppApiRecycleAppOrderReceive:
    """APP收货"""

    @pytest.mark.smoke
    def test_AppApiRecycleAppOrderReceive(self, api_session, login_tool):
        url = f"{APP_URL}/app-api/recycle/app/order/receive"
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        body = {"id": order_data['app_order']['order_id']}
        resp = api_session.post(url, json=body, headers=headers)
        assert resp.status_code == 200
