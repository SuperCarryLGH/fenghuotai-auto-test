import pytest
from config import ADMIN_URL


class TestProductSpuUpdateStatus:
    """更新商品 SPU Status"""

    @pytest.mark.smoke
    def test_ProductSpuUpdateStatus(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/product/spu/update-status"
        body = {"id": "2076547056304779266", "status": 0}
        ok(api_session.put(url, json=body, headers=auth_headers))
