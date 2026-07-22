import pytest
from config import ADMIN_URL


class TestMemberSocialUserWxaQrcode:
    """获得微信小程序码(base64 image)"""

    @pytest.mark.smoke
    def test_MemberSocialUserWxaQrcode(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/member/social-user/wxa-qrcode"
        body = {"id": 1}  # TODO: 补充参数
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
