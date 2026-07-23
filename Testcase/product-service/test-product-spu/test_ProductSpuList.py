import pytest
from config import ADMIN_URL


class TestProductSpuList:
    """获得商品 SPU 详情列表"""

    @pytest.mark.smoke
    def test_ProductSpuList(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/product/spu/list"
        params = {
            "spuIds": ["2076547056304779266"],
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
