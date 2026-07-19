import pytest
from config import ADMIN_URL


class TestProductSpuDelete:
    """删除商品 SPU"""

    @pytest.mark.smoke
    def test_ProductSpuDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/product/spu/delete"
        params = {"id": autotest_spu_id}  # 来自 conftest fixture
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
