import pytest
from config import APP_URL


class TestDistPromoterWallet:
    """获取推广员钱包"""
    URL = f"{APP_URL}/app-api/dist/wallet/wallet"
    @pytest.mark.smoke
    def test_DistPromoterWallet(self, api_session, promoter_headers, ok):
        r = ok(api_session.get(self.URL, headers=promoter_headers, params={"promoteType": 10}))
        print(r)
