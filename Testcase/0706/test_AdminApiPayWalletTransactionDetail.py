import pytest
from config import ADMIN_URL


class TestAdminApiPayWalletTransactionDetail:
    """获得钱包流水分页-新"""

    @pytest.mark.smoke
    def test_AdminApiPayWalletTransactionDetail(self, api_session, auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/pay/wallet-transaction/detail"
        params = {
            "id": "1024",  # [必填] 钱包流水编号
            "walletType": "10",  # [必填] 钱包类型 10-分拣中心 30-网点 40-用户
        }

        resp = api_session.get(url, headers=auth_headers, params=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        assert r["data"] is not None
        print(r)