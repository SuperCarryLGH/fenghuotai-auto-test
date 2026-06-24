import pytest
from config import APP_URL
from Common.login import Login
from Common.loader import load_recycle_apptransferOrder_calltransfernow

transfer = load_recycle_apptransferOrder_calltransfernow()


class Test_AdminApiRecycleAppTransferOrderGet:
    """转运订单详情"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAppTransferOrderGet(self, api_session, login_tool):
        mobile = "18600000002"
        token = login_tool.app_login(mobile=mobile)
        headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}

        url = f"{APP_URL}/admin-api/recycle/app-transferOrder/get"
        params ={
            "id": transfer["transfer"]['id']
            }
        resp = api_session.get(url, params=params, headers=headers)
        #assert resp.status_code == 200
        r = resp.json()
        #assert r["code"] == 0
        print(r)
