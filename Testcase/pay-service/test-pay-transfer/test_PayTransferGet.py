import pytest
from config import ADMIN_URL


class TestPayTransferGet:
    """获得转账订单"""

    @pytest.mark.smoke
    def test_PayTransferGet(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/pay/transfer/get"
        params = {"id": 15617637160}
        ok(api_session.get(url, params=params, headers=auth_headers))
