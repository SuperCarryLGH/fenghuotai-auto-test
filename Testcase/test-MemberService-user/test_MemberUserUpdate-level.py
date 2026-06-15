import pytest
from config import ADMIN_URL


class TestMemberUserUpdateLevel:
    """更新会员用户等级"""

    @pytest.mark.smoke
    def test_MemberUserUpdateLevel(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/member/user/update-level"
        params = {
            "id": "", #用户编号
            "levelId": "", #用户等级编号
            "reason": "", #修改原因
            }

        resp = api_session.put(url, headers=auth_headers,json=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] == {}
        print(r)








#test_AppApiCooperationGetByPlatform