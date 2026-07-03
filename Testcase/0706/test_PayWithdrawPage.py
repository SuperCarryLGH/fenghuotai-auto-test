import pytest
from config import ADMIN_URL
from Common.loader import load_pay_withdraw_page

page = load_pay_withdraw_page()


class TestPayWithdrawPage:
    """获得提现单分页"""

    @pytest.mark.smoke
    def test_PayWithdrawPage(self, api_session, auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/pay/withdraw/page"
        params = {
            "sourceType": page["page"]["sourceType"],
            "pageNo": page["page"]["pageNo"],
            "pageSize": page["page"]["pageSize"],
            "stationIdName": page["page"]["stationIdName"],
            "companyId": page["page"]["companyId"],
            "payChannelKey": page["page"]["payChannelKey"],
            "status": page["page"]["status"],
            "createTime": page["page"]["createTime"],
            "id": page["page"]["id"],
            "userId": page["page"]["userId"],
            "mobile": page["page"]["mobile"],
            "userType": page["page"]["userType"],
            "type": page["page"]["type"],
            "payAppKey": page["page"]["payAppKey"],
            "userAccount": page["page"]["userAccount"],
            "userName": page["page"]["userName"]
        }

        resp = api_session.get(url, headers=auth_headers, params=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] != {}
        print(r)








