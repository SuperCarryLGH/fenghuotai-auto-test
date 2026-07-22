import pytest
from config import ADMIN_URL


class TestAfterSaleUpdateRefunded:
    """更新售后订单为已退款"""

    @pytest.mark.smoke
    def test_AfterSaleUpdateRefunded(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/trade/after-sale/update-refunded"
        body = {"id": 1}  # TODO: 补充参数
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
