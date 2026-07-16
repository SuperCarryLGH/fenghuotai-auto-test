import pytest
from config import ADMIN_URL


class TestPropertyValueSimpleList:
    """获得属性值精简列表"""

    @pytest.mark.smoke
    def test_PropertyValueSimpleList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/product/property/value/simple-list"
        params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
