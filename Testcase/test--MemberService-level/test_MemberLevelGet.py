import pytest
from config import ADMIN_URL


class TestMemberLevelGet:
    """获取会员等级"""

    @pytest.mark.smoke
    def test_MemberLevelGet(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/member/level/get"
        params = {
            "id": 1
            }

        resp = api_session.get(url, headers=auth_headers,params=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] == {}
        print(r)








#test_AppApiCooperationGetByPlatform