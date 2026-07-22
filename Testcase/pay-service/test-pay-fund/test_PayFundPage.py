import pytest
from config import ADMIN_URL


class TestPayFundPage:
    """获得公司-分拣中心资金分页"""

    @pytest.mark.smoke
    def test_PayFundPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/fund/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
            "fundType" :20
        }
        print("url:",url)
        print("params:",params)
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
