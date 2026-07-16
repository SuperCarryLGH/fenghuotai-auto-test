import pytest
from config import ADMIN_URL


class TestProductPropertyDelete:
    """删除属性项"""

    @pytest.mark.smoke
    def test_ProductPropertyDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/product/property/delete"
        params = {"id": "product_property_id"}  # 来自 conftest fixture
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
