import pytest
from config import ADMIN_URL


class TestPropertyValueGet:
    """获得属性值"""

    @pytest.mark.smoke
    def test_PropertyValueGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/product/property/value/get"
        params = {"id": autotest_value_id}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
