import pytest
from config import ADMIN_URL


class TestPropertyValueCreate:
    """创建属性值"""

    @pytest.mark.smoke
    def test_PropertyValueCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/product/property/value/create"
        body = {"propertyId": 1, "name": f"商品_194199", "remark": "测试"}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
