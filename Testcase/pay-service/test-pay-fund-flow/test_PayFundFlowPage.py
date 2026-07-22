import pytest
from config import ADMIN_URL


class TestPayFundFlowPage:
    """获得资金流水分页"""

    @pytest.mark.smoke
    def test_PayFundFlowPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/fund-flow/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
            #"orgId":2074701657159761922
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
