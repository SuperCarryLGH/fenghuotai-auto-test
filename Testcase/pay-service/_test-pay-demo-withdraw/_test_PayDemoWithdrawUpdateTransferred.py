import pytest
from config import ADMIN_URL


class TestPayDemoWithdrawUpdateTransferred:
    """更新示例提现单的转账状态"""

    @pytest.mark.smoke
    def test_PayDemoWithdrawUpdateTransferred(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/demo-withdraw/update-transferred"
        body = {"id": "_pay_demo_withdraw_id"}  # 来自 conftest fixture
        resp = api_session.post(url, json=body, headers=auth_headers)
