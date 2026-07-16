import pytest
from config import ADMIN_URL


class TestProductCommentCreate:
    """添加自评"""

    @pytest.mark.smoke
    def test_ProductCommentCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/product/comment/create"
        body = {"name": f"商品_194199", "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
