import pytest
from config import ADMIN_URL


class TestPromotionArticleCategoryListAllSimple:
    """获取文章分类精简信息列表"""

    @pytest.mark.smoke
    def test_PromotionArticleCategoryListAllSimple(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/article-category/list-all-simple"
        params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
