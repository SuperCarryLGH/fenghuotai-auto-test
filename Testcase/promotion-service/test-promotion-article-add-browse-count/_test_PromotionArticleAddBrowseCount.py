import pytest
from config import APP_URL


class TestPromotionArticleAddBrowseCount:
    """增加文章浏览量"""

    @pytest.mark.smoke
    def test_PromotionArticleAddBrowseCount(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/promotion/article/add-browse-count"
        body = {"id": 1}  # TODO: 补充参数
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
