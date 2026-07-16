import pytest
from config import ADMIN_URL


class TestPromotionArticleUpdate:
    """更新文章管理"""

    @pytest.mark.smoke
    def test_PromotionArticleUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/article/update"
        body = {"id": "promotion_article_id"}  # 来自 conftest fixture
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
