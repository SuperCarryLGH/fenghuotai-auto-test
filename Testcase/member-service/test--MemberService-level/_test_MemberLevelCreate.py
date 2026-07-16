import pytest
from config import ADMIN_URL
from Common.loader import load_member_level_create
create = load_member_level_create()


class TestMemberLevelCreate:
    """创建会员等级"""

    @pytest.mark.smoke
    def test_MemberLevelCreate(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/member/level/create"
        params = {
            "name": create["create"]["name"],
            "experience": create["create"]["experience"],
            "level": create["create"]["level"],
            "discountPercent": create["create"]["discountPercent"],
            "icon": create["create"]["icon"],
            "backgroundUrl": create["create"]["backgroundUrl"],
            "status": create["create"]["status"],
            }

        resp = api_session.post(url, headers=auth_headers,json=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] == {}
        print(r)








#test_AppApiCooperationGetByPlatform