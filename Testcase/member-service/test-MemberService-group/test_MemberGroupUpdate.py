import pytest
from config import ADMIN_URL


class TestMemberGroupUpdate:
    """更新用户分组"""

    @pytest.mark.smoke
    def test_MemberGroupUpdate(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/member/group/update"
        params = {
            "name": "购物达人",  #名称
            "remark": "你猜", #备注
            "status": 1,
            "id": 20357
            }

        resp = api_session.put(url, headers=auth_headers,json=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] == {}
        print(r)








#test_AppApiCooperationGetByPlatform