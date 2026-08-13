import pytest
from config import ADMIN_URL


class TestAdminApiPayTransferOperateFund:
    """转账资金处理"""

    @pytest.mark.smoke
    def test_AdminApiPayTransferOperateFund(self, api_session, auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/rpc-api/pay/pay/transfer-operate-fund"
        payload = {
            "userId": 0,                                        # [必填] 用户ID
            "tradeChannel": 1,                                  # [必填] 结算渠道 1-微信 2-支付宝
            "amount": 10000,                                    # [必填] 结算金额，单位：分
            "bizNo": "1000000000",                              # [必填] 业务单号
            "thirdOrderNo": "4200001234202306010000000001",     # [必填] 第三方转账单号
        }

        resp = api_session.post(url, headers=auth_headers, json=payload)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        assert r["data"] is True
        print(r)
