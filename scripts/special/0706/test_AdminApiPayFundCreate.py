import pytest
from config import ADMIN_URL


class TestAdminApiPayFundCreate:
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
    def test_AdminApiPayFundCreate(self, api_session, auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/pay/fund/create"
        payload = {
                  "companyId": 100, #公司 ID（公司充值与分拣中心充值场景均必填）,示例值(100)
                  "sortingCenterId": 200,
                  "fundType": 10, #充值类型 10-公司充值 20-分拣中心充值,示例值(10)
                  "tradeChannel": 1, #充值渠道 1-微信 2-支付宝,示例值(1)
                  "rechargeAmount": 10000, #充值金额，单位：元,示例值(10000)
                  "voucherImgList": [],
                  "remark": "6 月充值",
                  "thirdNo": "4200001234202306010000000001",  #第三方充值单号（微信/支付宝订单号）,示例值(4200001234202306010000000001)
                  "bizNo": "FF202606180001"
                }

        resp = api_session.post(url, headers=auth_headers, json=payload)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        assert r["data"] is True
        print(r)