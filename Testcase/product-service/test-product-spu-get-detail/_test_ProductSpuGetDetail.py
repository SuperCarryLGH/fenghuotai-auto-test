import time

import pytest
from config import APP_URL
from Common.login import Login


class TestProductSpuGetDetail:
    """获得商品 SPU 明细"""

    @pytest.mark.smoke
    def test_ProductSpuGetDetail(self, api_session, login_tool):
        token = login_tool.app_login()
        headers = {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)), "Authorization": f"Bearer {token}"}
        url = f"{APP_URL}/app-api/product/spu/get-detail"
        params = {"id": "2076547056304779266"}
        resp = api_session.get(url, params=params, headers=headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
