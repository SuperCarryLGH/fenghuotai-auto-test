import pytest
from config import ADMIN_URL


class TestOrderGetByPickUpVerifyCode:
    """查询核销码对应的订单"""

    @pytest.mark.smoke
    @pytest.mark.skip(reason="需真实订单核销码，暂无有效参数")
    def test_OrderGetByPickUpVerifyCode(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/trade/order/get-by-pick-up-verify-code"
        params = {"id": 1}  # TODO: 补充查询参数
        resp = api_session.get(url, params=params, headers=auth_headers)
