import pytest
from config import ADMIN_URL


class TestProductPropertyDelete:
    """删除属性项"""

    @pytest.mark.smoke
    def test_ProductPropertyDelete(self, api_session, auth_headers, autotest_property_id, ok):
        url = f"{ADMIN_URL}/admin-api/product/property/delete"
        params = {"id": autotest_property_id}  # 来自 conftest fixture
        ok(api_session.delete(url, params=params, headers=auth_headers))
