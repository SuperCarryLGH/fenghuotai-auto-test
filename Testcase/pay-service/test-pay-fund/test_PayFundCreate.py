import pytest
import time
from config import ADMIN_URL


class TestPayFundCreate:
    """公司充值 - 分拣中心充值"""

    @pytest.fixture(autouse=True)
    def _cleanup(self, api_session, auth_headers):
        self._created_id = None
        yield
        if self._created_id is not None:
            try:
                api_session.delete(f"{ADMIN_URL}/admin-api/pay/fund/delete", params={"id": self._created_id}, headers=auth_headers)
            except Exception as e:
                print(f"[cleanup] 删除失败 {self._created_id}: {e}")


    @pytest.mark.smoke
    def test_PayFundCreate(self, api_session, auth_headers, ok):
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
        r = ok(api_session.post(url, json=body, headers=auth_headers))
        self._created_id = r["data"] if isinstance(r["data"], (int, str)) and not isinstance(r["data"], bool) else (r["data"].get("id") if isinstance(r["data"], dict) else None)
