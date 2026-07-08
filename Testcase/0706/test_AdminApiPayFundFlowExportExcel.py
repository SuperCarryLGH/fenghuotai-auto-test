import pytest
from config import ADMIN_URL


class TestAdminApiPayFundFlowExportExcel:
    """导出资金流水 Excel"""

    @pytest.mark.smoke
    def test_AdminApiPayFundFlowExportExcel(self, api_session, auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/pay/fund-flow/export-excel"
        params = {
            "pageNo": 1,  # 必填
            "pageSize": 10,  # 必填
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

        resp = api_session.get(url, headers=auth_headers, params=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)