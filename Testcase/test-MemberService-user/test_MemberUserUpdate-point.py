import pytest
from config import ADMIN_URL


class TestMemberUserUpdatePoint:
    """更新会员用户积分"""

    @pytest.mark.smoke
    def test_MemberUserUpdatePoint(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/member/user/update-point"
        params = {
            "id": "", #用户编号
            "point": "", #变动积分 正数为增加，负数为减少
            }

        resp = api_session.put(url, headers=auth_headers,json=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] == {}
        print(r)








#test_AppApiCooperationGetByPlatform