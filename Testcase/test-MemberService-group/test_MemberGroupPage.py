import pytest
from config import ADMIN_URL


class TestMemberGroupPage:
    """获得用户分组"""

    @pytest.mark.smoke
    def test_MemberGroupPage(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/member/group/page"
        params = {
            "PageNo": "1",
            "PageSize": "100",
            "name": "",  #名称
            "status": "",
            "creatTime": ""
            }

        resp = api_session.get(url, headers=auth_headers,params=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] == {}
        print(r)








#test_AppApiCooperationGetByPlatform