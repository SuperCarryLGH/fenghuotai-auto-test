import pytest
from config import ADMIN_URL


class TestPayDemoWithdrawCreate:
    """创建示例提现单"""

    @pytest.mark.smoke
    def test_PayDemoWithdrawCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/demo-withdraw/create"
        body = {"name": f"autotest_194200", "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
