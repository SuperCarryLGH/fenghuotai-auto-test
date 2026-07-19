import pytest
from config import ADMIN_URL


class TestPromotionSeckillConfigDelete:
    """删除秒杀时段"""

    @pytest.mark.smoke
    def test_PromotionSeckillConfigDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/seckill-config/delete"
        params = {"id": "promotion_seckill_config_id"}  # 来自 conftest fixture
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
