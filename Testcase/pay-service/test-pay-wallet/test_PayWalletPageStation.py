import time
import pytest
from config import ADMIN_URL, APP_URL
from Common.login import Login


@pytest.mark.skip(reason="接口返回 500 系统异常，待确认")
class TestPayWalletPageStation:
    """获得站点钱包流水分页"""

    @pytest.mark.smoke
    def test_PayWalletPageStation(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/pay/wallet/page-station"
        params = {"pageNo": 1, "pageSize": 10, "bizType": 11}
        ok(api_session.get(url, params=params, headers=auth_headers))
