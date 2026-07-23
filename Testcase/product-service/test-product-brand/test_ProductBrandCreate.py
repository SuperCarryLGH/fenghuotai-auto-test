import time
import pytest
from config import ADMIN_URL


class TestProductBrandCreate:
    """创建品牌"""

    @pytest.mark.smoke
    def test_ProductBrandCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/product/brand/create"
        body = {"name": f"品牌_{int(time.time())}", "picUrl": "", "sort": 0, "status": 0}
        ok(api_session.post(url, json=body, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
