import pytest
from config import ADMIN_URL


class TestSystemAuthAlipayAuthorizeBind:
    """支付宝应用授权，获取支付宝 userid"""

    @pytest.mark.smoke
    def test_SystemAuthAlipayAuthorizeBind(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/auth/alipay-authorize-bind"
        body = {"id": 1}  # TODO: 补充参数
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
