import pytest
from config import ADMIN_URL


class TestMemberExperienceRecordPage:
    """获得会员等级记录分页"""

    @pytest.mark.smoke
    def test_MemberExperienceRecordPage(self, api_session,auth_headers, ok):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/member/experience-record/page"
        params = {
            "pageNo": 1,
            "pageSize": 200,
            }

        ok(api_session.get(url, headers=auth_headers,params=params))








#test_AppApiCooperationGetByPlatform