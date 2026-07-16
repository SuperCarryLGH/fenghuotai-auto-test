import pytest
from config import ADMIN_URL


class TestProductSpuListAllSimple:
    """获得商品 SPU 精简列表"""

    @pytest.mark.smoke
    def test_ProductSpuListAllSimple(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/product/spu/list-all-simple"
        params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
