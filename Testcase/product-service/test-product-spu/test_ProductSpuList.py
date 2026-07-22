import pytest
from config import ADMIN_URL


class TestProductSpuList:
    """获得商品 SPU 详情列表"""

    @pytest.mark.smoke
    def test_ProductSpuList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/product/spu/list"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
