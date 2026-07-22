import pytest
from config import ADMIN_URL


class TestProductSpuGetCount:
    """获得商品 SPU 分页 tab count"""

    @pytest.mark.smoke
    def test_ProductSpuGetCount(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/product/spu/get-count"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
