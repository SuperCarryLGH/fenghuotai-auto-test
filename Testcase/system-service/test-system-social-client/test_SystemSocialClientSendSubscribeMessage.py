import pytest
from config import ADMIN_URL


class TestSystemSocialClientSendSubscribeMessage:
    """发送订阅消息"""

    @pytest.mark.smoke
    def test_SystemSocialClientSendSubscribeMessage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/social-client/send-subscribe-message"
        body = {"id": "id"}  # 来自 conftest fixture
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
