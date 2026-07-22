import pytest
from config import ADMIN_URL


class TestProductSpuUpdate:
    """更新商品 SPU"""

    @pytest.mark.smoke
    def test_ProductSpuUpdate(self, api_session, auth_headers, autotest_spu_id):
        url = f"{ADMIN_URL}/admin-api/product/spu/update"
        body = {"id": autotest_spu_id}  # 来自 conftest fixture
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
