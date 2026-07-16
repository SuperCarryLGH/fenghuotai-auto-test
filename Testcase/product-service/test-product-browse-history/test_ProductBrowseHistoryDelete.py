import pytest
from config import APP_URL


class TestProductBrowseHistoryDelete:
    """删除商品浏览记录"""

    @pytest.mark.smoke
    def test_ProductBrowseHistoryDelete(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/product/browse-history/delete"
        params = {"id": 1}  # TODO: 替换为实际要删除的 ID
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
