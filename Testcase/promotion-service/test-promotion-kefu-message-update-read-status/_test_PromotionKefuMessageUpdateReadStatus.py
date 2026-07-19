import pytest
from config import APP_URL


class TestPromotionKefuMessageUpdateReadStatus:
    """更新客服消息已读状态"""

    @pytest.mark.smoke
    def test_PromotionKefuMessageUpdateReadStatus(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/promotion/kefu-message/update-read-status"
        body = {"id": 1}  # TODO: 补充参数
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
