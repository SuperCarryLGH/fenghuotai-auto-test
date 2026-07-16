import pytest
from config import APP_URL


class TestPromotionArticleGet:
    """获得文章详情"""

    @pytest.mark.smoke
    def test_PromotionArticleGet(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/promotion/article/get"
        resp = api_session.head(url, headers=auth_headers)
        assert resp.status_code == 200
