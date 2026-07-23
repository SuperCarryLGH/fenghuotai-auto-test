import pytest
from config import ADMIN_URL


class TestProductPropertyUpdate:
    """更新属性项"""

    @pytest.mark.smoke
    def test_ProductPropertyUpdate(self, api_session, auth_headers, autotest_property_id, ok):
        url = f"{ADMIN_URL}/admin-api/product/property/update"
        body = {"id": autotest_property_id, "name": "autotest_property_updated"}
        ok(api_session.put(url, json=body, headers=auth_headers))
