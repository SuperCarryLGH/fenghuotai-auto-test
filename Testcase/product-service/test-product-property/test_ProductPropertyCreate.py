import pytest
from config import ADMIN_URL


class TestProductPropertyCreate:
    """创建属性项"""

    @pytest.mark.smoke
    def test_ProductPropertyCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/product/property/create"
        body = {"name": f"商品_194199", "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
