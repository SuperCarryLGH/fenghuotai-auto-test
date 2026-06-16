import pytest
from config import ADMIN_URL


class TestMemberSocialUserWxaqrcode:
    """获得微信小程序码"""

    @pytest.mark.smoke
    def test_MemberSocialUserWxaqrcode(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/member/social-user/wxa-qrcode"
        params = {
            "scene": "1001",
            "path": "pages/goods/index",
            "width": 430,
            "autoColor": "true",
            "checkPath": "true",
            "hyaline": "true"
            }

        resp = api_session.post(url, headers=auth_headers,json=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] == {}
        print(r)








#test_AppApiCooperationGetByPlatform