import pytest
from config import APP_URL
from Common.login import Login
from Common.loader import load_recycle_apptransferOrder_calltransfernow

transfer = load_recycle_apptransferOrder_calltransfernow()


class Test_AdminApiRecycleAppTransferOrderLoadingComplete:
    """装车完成"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAppTransferOrderLoadingComplete(self, api_session, login_tool):
        mobile = "18600000002"
        token = login_tool.app_login(mobile=mobile)
        headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}

        url = f"{APP_URL}/admin-api/recycle/app-transferOrder/loading-complete"
        params ={
            "id": transfer["transfer"]['id'],
            "driverName": transfer["transfer"]['driverName'],
            "driverPhone": transfer["transfer"]['driverPhone'],
            "driverLicensePlateNumber": transfer["transfer"]['driverLicensePlateNumber'],
            "loadPicUrls": transfer["transfer"]['loadPicUrls']
            }
        resp = api_session.post(url, json=params, headers=headers)
        #assert resp.status_code == 200
        r = resp.json()
        #assert r["code"] == 0
        print(r)
