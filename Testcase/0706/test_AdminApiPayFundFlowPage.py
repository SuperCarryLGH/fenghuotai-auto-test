from xxlimited import Null

import pytest
from config import ADMIN_URL
class TestAdminApiPayFundFlowPage:
    """获得资金流水分页"""

    @pytest.mark.smoke
    def test_AdminApiPayFundFlowPage(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/pay/fund-flow/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
            # "payFundId": "26729",
            # "bizNo": "FF202606180001",
            # "orgId": "2630",
            # "fundType": "10",
            # "flowType": "10",
            # "tradeChannel": "1",
            # "thirdOrderNo": "4200001234202306010000000001",
            # "beforeBalance": "10000",
            # "tradeAmount": "5000",
            # "afterBalance": "15000",
            # "voucherImgList": "",
            # "remark": "你猜",
            # "createTime": "",
        }

        resp = api_session.get(url, headers=auth_headers,params=params)
        assert resp.status_code == 200
        r = resp.json()
        max=r["data"]["total"]-1
        assert r["code"] == 0
        assert r["data"]["total"] != Null
        assert r["data"]["list"][max] != Null
        print(r)