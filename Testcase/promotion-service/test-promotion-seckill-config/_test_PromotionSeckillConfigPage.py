import pytest
from config import ADMIN_URL


class TestPromotionSeckillConfigPage:
    """获得秒杀时间段分页"""

    @pytest.mark.smoke
    def test_PromotionSeckillConfigPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/seckill-config/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
