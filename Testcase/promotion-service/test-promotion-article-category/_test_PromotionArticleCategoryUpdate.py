import pytest
from config import ADMIN_URL


class TestPromotionArticleCategoryUpdate:
    """更新文章分类"""

    @pytest.mark.smoke
    def test_PromotionArticleCategoryUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/article-category/update"
        body = {"id": "promotion_article_category_id"}  # 来自 conftest fixture
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
