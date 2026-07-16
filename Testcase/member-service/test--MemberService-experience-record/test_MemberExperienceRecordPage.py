import pytest
from config import ADMIN_URL


class TestMemberExperienceRecordPage:
    """获得会员经验记录分页"""

    @pytest.mark.smoke
    def test_MemberExperienceRecordPage(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/member/experience-record/page"
        params = {
            "PageNo": "1",
            "PageSize": "100",
            "userId": "", #用户编号
            "bizId": "", #业务编号
            "bizType": "", #业务类型
            "title": "", #标题
            "createTime": ""
            }

        resp = api_session.get(url, headers=auth_headers,params=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] == {}
        print(r)








#test_AppApiCooperationGetByPlatform