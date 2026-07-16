import pytest
from config import ADMIN_URL
from Common.loader import load_member_tag_list
list = load_member_tag_list()


class TestMemberTagList:
    """获得会员标签列表"""

    @pytest.mark.smoke
    def test_MemberTagList(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/member/tag/list"
        params = {
            "ids": list["list"]["ids"]
            }

        resp = api_session.get(url, headers=auth_headers,params=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] == [{'name': '绿色', 'id': 1, 'createTime': 1692494472000}, {'name': '黄色', 'id': 2, 'createTime': 1692494487000}]
        print(r)








#test_AppApiCooperationGetByPlatform