import pytest
from config import ADMIN_URL


class TestPromotionRewardActivityClose:
    """关闭满减送活动"""

    @pytest.mark.smoke
    def test_PromotionRewardActivityClose(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/reward-activity/close"
        body = {"id": 1}  # TODO: 补充参数
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
