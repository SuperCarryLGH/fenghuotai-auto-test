import pytest
from config import ADMIN_URL


class TestPromotionDiyPageList:
    """获得装修页面列表"""

    @pytest.mark.smoke
    def test_PromotionDiyPageList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/diy-page/list"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
