import pytest
from config import ADMIN_URL


class TestPayFundFlowGetByBizNo:
    """根据业务单号和流水类型获得资金流水"""

    @pytest.mark.smoke
    def test_PayFundFlowGetByBizNo(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/fund-flow/get-by-biz-no"
        params = {
            "bizNo":2077206234032902144,
            "flowType":10
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
