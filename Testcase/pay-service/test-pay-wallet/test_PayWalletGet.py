import pytest
from config import ADMIN_URL


class TestPayWalletGet:
    """获得用户钱包明细"""

    @pytest.mark.smoke
    def test_PayWalletGet(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/pay/wallet/get"
        params = {"userId": 2071418043802406914}
        ok(api_session.get(url, params=params, headers=auth_headers))
