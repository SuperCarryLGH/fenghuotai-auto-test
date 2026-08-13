import pytest
from config import ADMIN_URL


class TestPayRechargePage:
    """获得充值分页"""

    @pytest.mark.smoke
    def test_PayRechargePage(self, api_session, auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/pay/recharge/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }

        resp = api_session.get(url, headers=auth_headers, params=params)
        assert resp.status_code == 200
