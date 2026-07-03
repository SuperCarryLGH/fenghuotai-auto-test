import pytest
from config import ADMIN_URL


class TestAdminApiPayWithdrawOperateFund:
    """网点/用户提现"""

    @pytest.mark.smoke
    def test_AdminApiPayWithdrawOperateFund(self, api_session, auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/rpc-api/pay/pay/withdraw-operate-fund"
        payload = {
            "withdrawalType": 1,                                # [必填] 提现方 1-网点 2-用户
            "orgId": 1560,                                      # [必填] 机构ID（网点ID或用户ID）
            "amount": 10000,                                    # [必填] 提现金额，单位：分（≥1）
            "bizNo": "1000000000",                              # [必填] 业务单号
            "thirdOrderNo": "4200001234202306010000000001",     # [必填] 第三方提现单号（微信/支付宝订单号）
            "tradeChannel": 1,                                  # [必填] 提现渠道 1-微信 2-支付宝
        }

        resp = api_session.post(url, headers=auth_headers, json=payload)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        assert r["data"] is True
        print(r)
