import pytest
from config import ADMIN_URL


class TestMemberPointRecordPage:
    """获得会员配置"""

    @pytest.mark.smoke
    def test_MemberPointRecordPage(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/member/point/record/page"
        params = {
            "pageNo": "1", #页码
            "pageSize": "200", #每页条数
            "nickname": "", #用户昵称
            "userId": "", #用户编号
            "bizType": "", #业务类型
            "title": "" #积分标题
            }

        resp = api_session.get(url, headers=auth_headers,params=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] == {}
        print(r)








#test_AppApiCooperationGetByPlatform