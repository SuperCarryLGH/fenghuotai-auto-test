import pytest
from config import ADMIN_URL


class TestPayDemoOrderCreate:
    """创建示例订单"""

    @pytest.mark.smoke
    def test_PayDemoOrderCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/demo-order/create"
        body = {"name": f"autotest_194200", "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
