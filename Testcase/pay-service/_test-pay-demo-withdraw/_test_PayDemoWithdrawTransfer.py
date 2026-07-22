import pytest
from config import ADMIN_URL


class TestPayDemoWithdrawTransfer:
    """提现单转账"""

    @pytest.mark.smoke
    def test_PayDemoWithdrawTransfer(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/demo-withdraw/transfer"
        body = {"id": "_pay_demo_withdraw_id"}  # 来自 conftest fixture
        resp = api_session.post(url, json=body, headers=auth_headers)
