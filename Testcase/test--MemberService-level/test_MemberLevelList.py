import pytest
from config import ADMIN_URL


class TestMemberLevelList:
    """获取会员等级列表"""

    @pytest.mark.smoke
    def test_MemberLeveList(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/member/level/list"
        params = {
            "name": "青铜",
            "status": "0",
            }

        resp = api_session.get(url, headers=auth_headers,params=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] == {}
        print(r)








#test_AppApiCooperationGetByPlatform