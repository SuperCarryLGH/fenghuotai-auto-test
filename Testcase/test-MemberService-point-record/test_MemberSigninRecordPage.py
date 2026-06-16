import pytest
from config import ADMIN_URL


class TestMemberSigninRecordPage:
    """获得签到记录分页"""

    @pytest.mark.smoke
    def test_MemberSigninRecordPage(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/member/sign-in/record/page"
        params = {
            "pageNo": "1", #页码
            "pageSize": "200", #每页条数
            "nickname": "", #用户昵称
            "day": "", #第几天签到
            "userId": "", #用户编号
            "createTime": "", #签到时间
            }

        resp = api_session.get(url, headers=auth_headers,params=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] == {}
        print(r)








#test_AppApiCooperationGetByPlatform