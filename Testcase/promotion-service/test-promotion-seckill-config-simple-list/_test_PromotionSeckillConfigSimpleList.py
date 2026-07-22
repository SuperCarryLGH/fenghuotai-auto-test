import pytest
from config import ADMIN_URL


class TestPromotionSeckillConfigSimpleList:
    """获得所有开启状态的秒杀时段精简列表"""

    @pytest.mark.smoke
    def test_PromotionSeckillConfigSimpleList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/seckill-config/simple-list"
        params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
