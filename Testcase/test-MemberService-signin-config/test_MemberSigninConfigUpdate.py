import pytest
from config import ADMIN_URL


class TestMemberSigninConfigUpdate:
    """更新签到规则"""

    @pytest.mark.smoke
    def test_MemberSigninConfigUpdate(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/member/sign-in/config/update"
        params = {
            "day": 7, #签到第x天
            "point": 10, #奖励积分
            "experience": 10, #奖励经验
            "status": 1, #状态
            "id": 1 #规则自增主键
            }

        resp = api_session.put(url, headers=auth_headers,json=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] == {}
        print(r)








#test_AppApiCooperationGetByPlatform