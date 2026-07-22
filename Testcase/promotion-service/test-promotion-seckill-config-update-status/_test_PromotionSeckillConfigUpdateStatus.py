import pytest
from config import ADMIN_URL


class TestPromotionSeckillConfigUpdateStatus:
    """修改时段配置状态"""

    @pytest.mark.smoke
    def test_PromotionSeckillConfigUpdateStatus(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/seckill-config/update-status"
        body = {"id": 1, "status": 0}  # TODO: 替换为实际 ID 和状态值
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
