import pytest
from config import ADMIN_URL


class TestProductPropertySimpleList:
    """获得属性项精简列表"""

    @pytest.mark.smoke
    def test_ProductPropertySimpleList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/product/property/simple-list"
        params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
