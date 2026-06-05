import pytest
from config import APP_URL
from Common.loader import load_page
page = load_page()

class TestAppApiRecycleActivityMyList:
    """用户 APP - 发获取活动组信息及活动列表"""

    @pytest.mark.smoke
    def test_AppApiRecycleActivityMyList(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{APP_URL}/app-api/recycle/activity/my/list"
        params = {
            "pageNo":page["page"]["pageNo"],
            "pageSize":page["page"]["pageSize"],
            "activityGroupId":1
            }

        resp = api_session.get(url, headers=auth_headers,params=params)
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        #assert data["data"]["id"] == 0
        print(data)



#AppApiRecycleActivityGroupDetail