import pytest
from config import ADMIN_URL


class TestProductCommentUpdateVisible:
    """显示 - 隐藏评论"""

    @pytest.mark.smoke
    def test_ProductCommentUpdateVisible(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/product/comment/update-visible"
        body = {"id": 1}  # TODO: 补充参数
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
