import pytest
from config import APP_URL


class TestPromotionArticlePage:
    """获得文章详情分页"""

    @pytest.mark.smoke
    def test_PromotionArticlePage(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/promotion/article/page"
        resp = api_session.head(url, headers=auth_headers)
        assert resp.status_code == 200
