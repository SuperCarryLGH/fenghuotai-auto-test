import pytest
from config import APP_URL


class TestMemberAuthCreateWeixinJsapiSignature:
    """创建微信 JS SDK 初始化所需的签名"""

    @pytest.mark.smoke
    def test_MemberAuthCreateWeixinJsapiSignature(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/member/auth/create-weixin-jsapi-signature"
        body = {
            # TODO: 补充请求体参数
        }
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)

 == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
