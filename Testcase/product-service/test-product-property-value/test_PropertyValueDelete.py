import pytest
from config import ADMIN_URL


class TestPropertyValueDelete:
    """删除属性值"""

    @pytest.mark.smoke
    def test_PropertyValueDelete(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/product/property/value/delete"
        params = {"id": autotest_value_id}  # 来自 conftest fixture
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
