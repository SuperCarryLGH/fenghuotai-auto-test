import pytest
from config import APP_URL


class TestPromotionArticleCategoryList:
    """获得文章分类列表"""

    @pytest.mark.smoke
    def test_PromotionArticleCategoryList(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/promotion/article-category/list"
        resp = api_session.head(url, headers=auth_headers)
        assert resp.status_code == 200
