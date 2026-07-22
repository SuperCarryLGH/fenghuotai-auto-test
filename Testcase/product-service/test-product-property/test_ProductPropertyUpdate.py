import pytest
from config import ADMIN_URL


class TestProductPropertyUpdate:
    """更新属性项"""

    @pytest.mark.smoke
    def test_ProductPropertyUpdate(self, api_session, auth_headers, autotest_property_id):
        url = f"{ADMIN_URL}/admin-api/product/property/update"
        body = {"id": autotest_property_id}  # 来自 conftest fixture
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
