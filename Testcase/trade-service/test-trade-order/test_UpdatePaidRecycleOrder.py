import pytest
from config import ADMIN_URL


class TestUpdatePaidRecycleOrder:
    """更新回收订单为已支付"""

    @pytest.mark.smoke
    def test_UpdatePaidRecycleOrder(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/update-paid-recycle-order"
        body = {
            # TODO: 补充请求体参数
        }
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
