import pytest
from config import ADMIN_URL
from Common.loader import load_member_tag_delete
delete = load_member_tag_delete()


class TestMemberTagDelete:
    """删除会员标签"""

    @pytest.mark.smoke
    def test_MemberTagDelete(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/member/tag/delete"
        params = {
            "id": delete["delete"]["id"]
            }

        resp = api_session.delete(url, headers=auth_headers,params=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] == {}
        print(f"删除的标签ID: {delete['delete']['id']}")
        print(r)








#test_AppApiCooperationGetByPlatform