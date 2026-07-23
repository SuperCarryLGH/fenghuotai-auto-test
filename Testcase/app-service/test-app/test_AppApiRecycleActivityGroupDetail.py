import time
import pytest
from config import APP_URL
from Common.login import Login
from Common.loader import load_users, load_common
users = load_users()
common = load_common()

class TestAppApiRecycleActivityGroupDetail:
    """用户 APP - 发获取活动组信息及活动列表"""

    @pytest.mark.smoke
    def test_AppApiRecycleActivityGroupDetail(self, api_session, login_tool, ok):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/recycle/activity/group/detail"
        params = {
                    "groupId": 1
            }

        ok(api_session.get(url, headers=headers,params=params))
        r = resp.json()
        assert r["code"] == 0
        assert r["data"]["id"] == 1
        print(r)



#AppApiRecycleActivityGroupDetail