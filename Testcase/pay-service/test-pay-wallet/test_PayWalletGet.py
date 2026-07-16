import pytest
from config import ADMIN_URL


class TestPayWalletGet:
    """获得用户钱包明细"""

    @pytest.mark.smoke
    def test_PayWalletGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/wallet/get"
        params = {"id": 1}  # TODO: 替换为实际存在的 ID
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
