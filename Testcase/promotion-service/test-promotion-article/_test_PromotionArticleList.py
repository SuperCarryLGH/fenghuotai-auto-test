import pytest
from config import APP_URL


class TestPromotionArticleList:
    """获得文章详情列表"""

    @pytest.mark.smoke
    def test_PromotionArticleList(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/promotion/article/list"
        resp = api_session.head(url, headers=auth_headers)
        assert resp.status_code == 200
