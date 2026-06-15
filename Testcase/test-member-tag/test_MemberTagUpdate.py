import pytest
from config import ADMIN_URL
from Common.loader import load_member_tag_update
update = load_member_tag_update()


class TestMemberTagUpdate:
    """更新会员标签"""

    @pytest.mark.smoke
    def test_MemberTagUpdate(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/member/tag/update"
        params = {
            "name": update["update"]["name"],
            "id": update["update"]["id"],
            }

        resp = api_session.put(url, headers=auth_headers,json=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] == [{'name': '绿色', 'id': 1, 'createTime': 1692494472000}, {'name': '黄色', 'id': 2, 'createTime': 1692494487000}]
        print(r)








#test_AppApiCooperationGetByPlatform