import pytest
from config import ADMIN_URL


class TestProductSpuUpdateStatus:
    """更新商品 SPU Status"""

    @pytest.mark.smoke
    def test_ProductSpuUpdateStatus(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/product/spu/update-status"
        body = {"id": "2076547056304779266", "status": 0}
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
