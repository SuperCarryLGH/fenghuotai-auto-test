import pytest
from config import ADMIN_URL


class TestPayRefundGet:
    """获得退款订单"""

    @pytest.mark.smoke
    def test_PayRefundGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/refund/get"
        params = {"id": 1}  # TODO: 替换为实际存在的 ID
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
