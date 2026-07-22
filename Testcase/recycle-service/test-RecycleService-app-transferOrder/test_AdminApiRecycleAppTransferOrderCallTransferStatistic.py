import pytest
from config import APP_URL
from Common.login import Login


class Test_AdminApiRecycleAppTransferOrderCallTransferStatistic:
    """呼叫转运数据统计（在库重量、统货-黑料、前置仓与分拣中心信息）"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAppTransferOrderCallTransferStatistic(self, api_session, login_tool):
        mobile = "18600000002"
        token = login_tool.app_login(mobile=mobile)
        headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}

        url = f"{APP_URL}/admin-api/recycle/app-transferOrder/call-transfer-statistic"
        params ={
            "": ""
            }
        resp = api_session.get(url, params=params, headers=headers)
        #assert resp.status_code == 200
        r = resp.json()
        #assert r["code"] == 0
        print(r)
