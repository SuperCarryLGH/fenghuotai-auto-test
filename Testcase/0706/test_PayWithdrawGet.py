import pytest
from config import ADMIN_URL



class TestPayWithdrawGet:
    """获得提现单详情"""

    @pytest.mark.smoke
    def test_PayWithdrawGet(self, api_session, auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/pay/withdraw/get"
        params = {
            "id": ""
        }

        resp = api_session.get(url, headers=auth_headers, params=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] != {}
        print(r)








