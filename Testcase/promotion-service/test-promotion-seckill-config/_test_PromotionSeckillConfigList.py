import pytest
from config import APP_URL


class TestPromotionSeckillConfigList:
    """获得秒杀时间段列表"""

    @pytest.mark.smoke
    def test_PromotionSeckillConfigList(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/promotion/seckill-config/list"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
