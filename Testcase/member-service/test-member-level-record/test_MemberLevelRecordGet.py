import pytest
from config import ADMIN_URL


class TestMemberLevelRecordGet:
    """获得会员等级记录"""

    @pytest.mark.smoke
    def test_MemberLeveRecordGet(self, api_session,auth_headers, ok):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/member/level-record/get"
        params = {
            "id": 1
            }

        ok(api_session.get(url, headers=auth_headers,params=params))
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] == {}
        print(r)








#test_AppApiCooperationGetByPlatform