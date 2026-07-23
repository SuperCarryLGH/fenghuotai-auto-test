import pytest
from config import ADMIN_URL


class TestProductPropertyGet:
    """获得属性项"""

    @pytest.mark.smoke
    def test_ProductPropertyGet(self, api_session, auth_headers, autotest_property_id, ok):
        url = f"{ADMIN_URL}/admin-api/product/property/get"
        params = {"id": autotest_property_id}  # 来自 conftest fixture
        ok(api_session.get(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
