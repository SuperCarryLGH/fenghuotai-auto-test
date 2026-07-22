import pytest
from config import ADMIN_URL


class TestPayWalletUpdateBalance:
    """更新会员用户余额"""

    @pytest.mark.smoke
    def test_PayWalletUpdateBalance(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/wallet/update-balance"
        body = {"userId": 15617637160, "balance": 0}  # 敏感操作,确认后执行
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
