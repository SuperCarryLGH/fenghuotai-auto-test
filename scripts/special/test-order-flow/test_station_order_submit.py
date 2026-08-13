import pytest
import time
from config import APP_URL
from Common.login import Login


@pytest.mark.skip(reason="依赖 member/address/create 前置数据，暂不维护")
class Teststation_order_submit:
    """"""

    @pytest.mark.smoke
    def test_station_order_submit(self, api_session, login_tool, autotest_address_id):
        url = f"{APP_URL}/app-api/recycle/order/station-order-submit"
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        params = {"id": autotest_address_id}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
