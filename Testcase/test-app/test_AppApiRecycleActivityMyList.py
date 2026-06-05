import pytest
from config import APP_URL
from Common.loader import load_page, load_common
page = load_page()
common = load_common()

class TestAppApiRecycleActivityMyList:
    """用户 APP - 发获取活动组信息及活动列表"""

    @pytest.mark.smoke
    def test_AppApiRecycleActivityMyList(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{APP_URL}/app-api/recycle/activity/my/list"
        params = {
            "pageNo": common['common']['page']['pageNo'],
            "pageSize": common['common']['page']['pageSize'],
            "activityGroupId":1
            }

        resp = api_session.get(url, headers=auth_headers,params=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"]["id"] == 0
        print(r)



#AppApiRecycleActivityGroupDetail