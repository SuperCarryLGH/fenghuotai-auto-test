import pytest
from config import ADMIN_URL


class TestPromotionArticleCategoryGet:
    """获得文章分类"""

    @pytest.mark.smoke
    def test_PromotionArticleCategoryGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/article-category/get"
        params = {"id": "promotion_article_category_id"}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
