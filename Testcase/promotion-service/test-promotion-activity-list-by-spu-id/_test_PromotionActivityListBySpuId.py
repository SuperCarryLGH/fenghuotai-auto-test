import pytest
from config import APP_URL


class TestPromotionActivityListBySpuId:
    """获得单个商品，进行中的拼团、秒杀、砍价活动信息"""

    @pytest.mark.smoke
    def test_PromotionActivityListBySpuId(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/promotion/activity/list-by-spu-id"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
