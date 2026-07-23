import pytest
from config import ADMIN_URL


class TestPayWalletGetWallettransactionDetail:
    """获得钱包流水详情"""

    @pytest.mark.smoke
    def test_PayWalletGetWallettransactionDetail(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/pay/wallet/get-walletTransaction-detail"
        params = {"id": "2079738455900680194",
                  "bizType": "11"
                  }
        ok(api_session.get(url, params=params, headers=auth_headers))
        r = resp.json()
        #assert r["code"] == 0
        print(r)
