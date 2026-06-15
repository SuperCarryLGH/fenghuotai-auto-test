import pytest
from config import ADMIN_URL
from Common.loader import load_common
common = load_common()


class TestMemberLevelRecordGet:
    """获得会员等级记录"""

    @pytest.mark.smoke
    def test_MemberLevelRecordGet(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/member/level-record/get"
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