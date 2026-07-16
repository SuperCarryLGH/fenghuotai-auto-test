import pytest
from config import APP_URL


class TestProductSpuGetDetail:
    """获得商品 SPU 明细"""

    @pytest.mark.smoke
    def test_ProductSpuGetDetail(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/product/spu/get-detail"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
