import pytest
from config import ADMIN_URL


class TestAdminApiPayChargeOperateFund:
    """网点充值 充值资金处理"""

    @pytest.mark.smoke
    def test_AdminApiPayChargeOperateFund(self, api_session, auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/rpc-api/pay/pay/charge-operate-fund"
        payload = {
            "orgId": 2061713873303195650,                                      # [必填] 网点ID
            "tradeChannel": 1,                                  # [必填] 充值渠道 1-微信 2-支付宝
            "rechargeAmount": 1,                            # [必填] 充值金额，单位：分（≥1）
            "thirdNo": "4200001234202306012345678901",          # [必填] 第三方充值单号（微信/支付宝订单号）
            "bizNo": "1000000000",                              # [必填] 业务单号
        }

        resp = api_session.post(url, headers=auth_headers, json=payload)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        assert r["data"] is True
        print(r)
