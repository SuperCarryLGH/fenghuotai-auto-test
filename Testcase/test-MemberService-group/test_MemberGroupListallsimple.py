import pytest
from config import ADMIN_URL


class TestMemberGroupListallsimple:
    """获取会员分组精简信息列表"""

    @pytest.mark.smoke
    def test_MemberGroupListallsimple(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/member/group/listallsimple"
        params = {
            "": ""
            }

        resp = api_session.get(url, headers=auth_headers,params=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] == {}
        print(r)








#test_AppApiCooperationGetByPlatform