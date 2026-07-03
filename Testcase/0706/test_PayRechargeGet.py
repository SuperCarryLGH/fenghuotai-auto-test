import pytest
from config import ADMIN_URL
from Common.loader import load_pay_recharge_export

export = load_pay_recharge_export()


class TestPayRechargeGet:
    """充值详情"""

    @pytest.mark.smoke
    def test_PayRechargeGet(self, api_session, auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/pay/recharge/get"
        params = {
            "id": export["export"]["id"],  # 流水id
            "centerIdOrName": export["export"]["centerIdOrName"],  # 网点名称/ID
            "flowType": export["export"]["flowType"],  # 公司充值 10 网点充值30
            "companyId": export["export"]["companyId"],  # 公司ID
            "accountingCompanyId": export["export"]["accountingCompanyId"],  # 入账公司
            "tradeChannel": export["export"]["tradeChannel"],  # 充值渠道：1-微信 2-支付宝
            "createTime": export["export"]["createTime"],  # 充值时间范围
            "payStatus": export["export"]["payStatus"]  # 状态：支付成功 未支付
        }

        resp = api_session.get(url, headers=auth_headers, params=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] != {}
        print(r)








