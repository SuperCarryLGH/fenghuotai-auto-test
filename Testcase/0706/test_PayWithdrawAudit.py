import pytest
from config import ADMIN_URL
from Common.loader import load_pay_withdraw_audit

audit = load_pay_withdraw_audit()


class TestPayWithdrawAudit:
    """获得提现单分页"""

    @pytest.mark.smoke
    def test_PayWithdrawAudit(self, api_session, auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/pay/withdraw/audit"
        params = {
            "withdrawId": audit["audit"]["withdrawId"],
            "approve": audit["audit"]["approve"],
            "remark": audit["audit"]["remark"],
            "sourceType": audit["audit"]["sourceType"]
        }

        resp = api_session.put(url, headers=auth_headers, json=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] != {}
        print(r)








