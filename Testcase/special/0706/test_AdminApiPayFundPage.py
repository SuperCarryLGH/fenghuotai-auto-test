import pytest
from config import ADMIN_URL


class TestAdminApiPayFundPage:
    """获得公司-分拣中心资金分页"""

    @pytest.mark.smoke
    def test_AdminApiPayFundPage(self, api_session, auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/pay/fund/page"
        params = {
                  "pageNo": 100, #	页码，从 1 开始,示例值(1)
                  "pageSize": 200, #每页条数，最大值为 200,示例值(10)
                  #"fundType": 10, #充值类型 10-公司充值 20-分拣中心充值,示例值(10)
                  #"orgId": 1, #机构ID,示例值(23468)
                  #"companyId": 10000, #所属公司ID,示例值(23468)
                  #"totalFund": [],
                  #"wechatFund": "6 月充值",
                  #"alipayFund": "4200001234202306010000000001",  #第三方充值单号（微信/支付宝订单号）,示例值(4200001234202306010000000001)
                  #"allocableFund": "FF202606180001",
                  #"allocatedFund":"",
                  #"createTime":""
                }

        resp = api_session.get(url, headers=auth_headers, params=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        assert r["data"]["total"] > 0
        assert len(r["data"]["list"]) > 0
        print(r)