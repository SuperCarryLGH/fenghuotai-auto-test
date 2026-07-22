import pytest
from config import ADMIN_URL


class TestProductCommentPage:
    """获得商品评价分页"""

    @pytest.mark.smoke
    def test_ProductCommentPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/product/comment/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
