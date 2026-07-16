import pytest
from config import ADMIN_URL
from Common.loader import load_member_tag_get
get = load_member_tag_get()


class TestMemberTagGet:
    """获得会员标签"""

    @pytest.mark.smoke
    def test_MemberTagGet(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/member/tag/get"
        params = {
            "id": get["get"]["id"]
            }

        resp = api_session.get(url, headers=auth_headers,params=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] == {}
        print(r)








#test_AppApiCooperationGetByPlatform