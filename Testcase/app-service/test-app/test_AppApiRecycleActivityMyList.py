import pytest
from config import APP_URL
from Common.login import Login
from Common.loader import load_page, load_common
page = load_page()
common = load_common()

class TestAppApiRecycleActivityMyList:
    """用户 APP - 发获取活动组信息及活动列表"""

    @pytest.mark.smoke
    def test_AppApiRecycleActivityMyList(self, api_session, login_tool, ok):
        mobile = "15617617160"
        token = login_tool.app_login(mobile=mobile)
        headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/recycle/activity/my/list"
        params = {
            "pageNo": common['common']['page']['pageNo'],
            "pageSize": common['common']['page']['pageSize'],
            "activityId": "12",
            #"activityGroupId":1
            }
        print(params)

        ok(api_session.get(url, headers=headers,params=params))
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"]["id"] == 0
        print(r)



#AppApiRecycleActivityGroupDetail