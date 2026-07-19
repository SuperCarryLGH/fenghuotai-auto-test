import pytest
from config import ADMIN_URL


class TestSystemAuthWechatAuthorizeBind:
    """微信授权，获取微信 openid"""

    @pytest.mark.smoke
    def test_SystemAuthWechatAuthorizeBind(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/auth/wechat-authorize-bind"
        body = {"id": 1}  # TODO: 补充参数
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
