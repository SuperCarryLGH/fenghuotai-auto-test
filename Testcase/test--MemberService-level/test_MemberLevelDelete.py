import pytest
from config import ADMIN_URL


class TestMemberLevelDelete:
    """删除会员等级"""

    @pytest.mark.smoke
    def test_MemberLevelDelete(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/member/level/delete"
        params = {
            "id": 2
            }

        resp = api_session.delete(url, headers=auth_headers,params=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] == {}
        print(r)








#test_AppApiCooperationGetByPlatform