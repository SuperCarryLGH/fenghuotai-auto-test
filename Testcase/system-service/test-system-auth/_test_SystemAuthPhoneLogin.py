import pytest
from config import ADMIN_URL


class TestSystemAuthPhoneLogin:
    """使用手机号一键登录（阿里云 PNVS）"""

    @pytest.mark.smoke
    def test_SystemAuthPhoneLogin(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/auth/phone-login"
        body = {"id": 1}  # TODO: 补充参数
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
