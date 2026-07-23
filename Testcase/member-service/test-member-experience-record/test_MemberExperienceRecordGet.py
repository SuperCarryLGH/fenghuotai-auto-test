import pytest
from config import ADMIN_URL


class TestMemberExperienceRecordGet:
    """获得会员经验记录"""

    @pytest.mark.smoke
    def test_MemberExperienceRecordGet(self, api_session,auth_headers, ok):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/member/experience-record/get"
        params = {
            "id": 1
            }

        ok(api_session.get(url, headers=auth_headers,params=params))
        #assert r["data"] == {}
        print(r)








#test_AppApiCooperationGetByPlatform