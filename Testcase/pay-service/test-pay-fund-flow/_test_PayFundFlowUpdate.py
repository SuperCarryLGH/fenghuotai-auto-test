import pytest
from config import ADMIN_URL


class TestPayFundFlowUpdate:
    """更新资金流水"""

    @pytest.mark.smoke
    def test_PayFundFlowUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/fund-flow/update"
        body = {
              "id": 20945,
              "payFundId": 26729,
              "bizNo": "FF202606180001",
              "orgId": 2630,
              "flowType": 2,
              "tradeChannel": 1,
              "thirdOrderNo": "4200001234202306010000000001",
              "beforeBalance": 10000,
              "tradeAmount": 5000,
              "afterBalance": 15000,
              "voucherImgList": "",
              "remark": "你猜"
            }
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
