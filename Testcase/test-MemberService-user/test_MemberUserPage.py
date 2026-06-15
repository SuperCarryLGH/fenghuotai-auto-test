import pytest
from config import ADMIN_URL


class TestMemberUserPage:
    """获得会员用户分页"""

    @pytest.mark.smoke
    def test_MemberUserPage(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/member/user/page"
        params = {
            "PageNo": "1",
            "PageSize": "100",
            "mobile": "", #手机号
            "nickname": "", #用户昵称
            "loginDate": "", #最后登录时间
            "createTime": "", #创建时间
            "tagIds": "", #会员标签编号列表
            "levelId": "", #会员等级编号
            "groupId": "", #用户分组编号
            }

        resp = api_session.get(url, headers=auth_headers,params=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] == {}
        print(r)








#test_AppApiCooperationGetByPlatform