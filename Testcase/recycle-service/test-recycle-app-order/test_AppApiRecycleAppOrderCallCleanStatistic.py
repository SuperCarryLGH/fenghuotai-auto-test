import pytest
import time
from config import APP_URL
from Common.loader import load_common
from Common.loader import load_recycle_app_order
from Common.login import Login

common = load_common()
order_data = load_recycle_app_order()


class Test_AppApiRecycleAppOrderCallCleanStatistic:
    """APP呼叫清洁统计"""

    @pytest.mark.smoke
    def test_AppApiRecycleAppOrderCallCleanStatistic(self, api_session, login_tool):
        url = f"{APP_URL}/app-api/recycle/app/order/call-clean-statistic"
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        resp = api_session.get(url, headers=headers)
        assert resp.status_code == 200
