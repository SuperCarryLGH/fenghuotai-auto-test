import pytest
from config import ADMIN_URL


class TestPromotionArticleCategoryCreate:
    """创建文章分类"""

    @pytest.mark.smoke
    def test_PromotionArticleCategoryCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/promotion/article-category/create"
        body = {"name": f"autotest_194200", "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
