import pytest
from config import ADMIN_URL


class TestPropertyValueCreate:
    """创建属性值"""

    @pytest.mark.smoke
    def test_PropertyValueCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/product/property/value/create"
        body = {"propertyId": 1, "name": f"商品_194199", "remark": "测试"}
        ok(api_session.post(url, json=body, headers=auth_headers))
