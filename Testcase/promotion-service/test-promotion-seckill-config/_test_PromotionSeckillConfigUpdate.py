import pytest
from config import ADMIN_URL


class TestPromotionSeckillConfigUpdate:
    """更新秒杀时段"""

    @pytest.mark.smoke
    def test_PromotionSeckillConfigUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/seckill-config/update"
        body = {"id": "promotion_seckill_config_id"}  # 来自 conftest fixture
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
