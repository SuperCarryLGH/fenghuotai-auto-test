import pytest
from config import APP_URL


class TestProductBrowseHistoryClean:
    """清空商品浏览记录"""

    @pytest.mark.smoke
    def test_ProductBrowseHistoryClean(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/product/browse-history/clean"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
