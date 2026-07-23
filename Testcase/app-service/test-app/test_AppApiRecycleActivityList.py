import time
import pytest
from config import APP_URL
from Common.login import Login
from Common.loader import load_page, load_common
page = load_page()
common = load_common()

class TestAppApiRecycleActivityList:
    """用户 APP - 查询活动分页列表"""

    @pytest.mark.smoke
    def test_AppApiRecycleActivityList(self, api_session, login_tool, ok):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/recycle/activity/list"
        params = {
            "pageNo": common['common']['page']['pageNo'],
            "pageSize": common['common']['page']['pageSize'],
            "activityGroupId":1
            }

        ok(api_session.get(url, headers=headers,params=params))
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"]["id"] == 0
        print(r)



#AppApiRecycleActivityGroupDetail