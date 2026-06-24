import pytest
from config import APP_URL
from Common.login import Login
from Common.loader import load_recycle_apptransferOrder_calltransfernow

transfer = load_recycle_apptransferOrder_calltransfernow()


class Test_AdminApiRecycleAppTransferOrderAddPackage:
    """扫码新增转运包裹"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAppTransferOrderAddPackage(self, api_session, login_tool):
        mobile = "18600000002"
        token = login_tool.app_login(mobile=mobile)
        headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}

        url = f"{APP_URL}/admin-api/recycle/app-transferOrder/add-package"
        params ={
            "transferOrderId": transfer["transfer"]['transferOrderId'],
            "packageNo": transfer["transfer"]['packageNo'],
        }
        resp = api_session.post(url, json=params, headers=headers)
        #assert resp.status_code == 200
        r = resp.json()
        #assert r["code"] == 0
        print(r)
