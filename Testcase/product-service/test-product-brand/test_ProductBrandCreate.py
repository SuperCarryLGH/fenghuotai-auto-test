import time
import pytest
from config import ADMIN_URL


class TestProductBrandCreate:
    """创建品牌"""

    @pytest.mark.smoke
    def test_ProductBrandCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/product/brand/create"
        body = {"name": f"品牌_{int(time.time())}", "picUrl": "", "sort": 0, "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
