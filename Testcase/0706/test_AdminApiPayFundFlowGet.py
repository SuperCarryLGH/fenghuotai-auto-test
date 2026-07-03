from xxlimited import Null

import pytest
from config import ADMIN_URL
class TestAdminApiPayFundFlowGet:
    """获得资金流水"""

    @pytest.mark.smoke
    def test_AdminApiPayFundFlowGet(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/pay/fund-flow/get"
        params = {
            "id": 1024,
        }

        resp = api_session.get(url, headers=auth_headers,params=params)
        assert resp.status_code == 200
        r = resp.json()
        max=r["data"]["total"]-1
        assert r["code"] == 0
        assert r["data"]!= Null
        print(r)