import pytest
import time
from config import ADMIN_URL


class TestPayFundCreate:
    """公司充值 - 分拣中心充值"""

    @pytest.mark.smoke
    def test_PayFundCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/pay/fund/create"
        body = {
          "companyId": 2,
          "sortingCenterId": 2074701657159761922,
          "fundType": 20,
          "tradeChannel": 1,  #1是微信 2是支付宝
          "rechargeAmount": 100,
          #"voucherImgList": [],
          "remark": "6 月充值",
          "thirdNo": str(int(time.time())),
          #"bizNo": "FF202606180001"
        }
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
