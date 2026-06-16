import pytest
from config import ADMIN_URL


class TestMemberSigninConfigCreate:
    """创建签到规则"""

    @pytest.mark.smoke
    def test_MemberSigninConfigCreate(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/member/sign-in/config/create"
        params = {
            "day": 7, #签到第x天
            "point": 10, #奖励积分
            "experience": 10, #奖励经验
            "status": 1 #状态
            }

        resp = api_session.post(url, headers=auth_headers,json=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] == {}
        print(r)








#test_AppApiCooperationGetByPlatform