import pytest
from config import ADMIN_URL


class TestPropertyValueUpdate:
    """更新属性值"""

    @pytest.mark.smoke
    def test_PropertyValueUpdate(self, api_session, auth_headers, autotest_value_id, ok):
        url = f"{ADMIN_URL}/admin-api/product/property/value/update"
        body = {"id": autotest_value_id, "propertyId": 1, "name": "autotest_value_updated", "remark": "测试"}
        ok(api_session.put(url, json=body, headers=auth_headers))
