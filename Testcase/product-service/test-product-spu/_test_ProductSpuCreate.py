import pytest
from config import ADMIN_URL


class TestProductSpuCreate:
    """创建商品 SPU"""

    @pytest.mark.smoke
    def test_ProductSpuCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/product/spu/create"
        body = {"name": f"商品_194199", "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
