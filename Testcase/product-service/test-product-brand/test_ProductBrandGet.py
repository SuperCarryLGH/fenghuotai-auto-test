import pytest
from config import ADMIN_URL


class TestProductBrandGet:
    """获得品牌"""

    @pytest.mark.smoke
    def test_ProductBrandGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/product/brand/get"
        params = {"id": autotest_brand_id}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
