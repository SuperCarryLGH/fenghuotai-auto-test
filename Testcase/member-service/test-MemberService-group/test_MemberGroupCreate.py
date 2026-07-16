import pytest
from config import ADMIN_URL


class TestMemberGroupCreate:
    """创建用户分组"""

    @pytest.mark.smoke
    def test_MemberGroupCreate(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/member/group/create"
        params = {
            "name": "购物达人",
            "remark": "你猜",
            "status": 1
            }

        resp = api_session.post(url, headers=auth_headers,json=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] == {}
        print(r)








#test_AppApiCooperationGetByPlatform