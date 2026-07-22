import pytest
from config import ADMIN_URL


class TestAdminApiPayWalletTransactionWalletTranPage:
    """获得钱包流水分页-新"""

    @pytest.mark.smoke
    def test_AdminApiPayWalletTransactionWalletTranPage(self, api_session, auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/pay/wallet-transaction/walletTranPage"
        params = {
            "pageNo": 1,  # [必填] 页码，从1开始
            "pageSize": 10,  # [必填] 每页条数，最大200
            # "walletId": "888",         # 钱包编号
            # "bizType": "1024",         # 清运结算/回收结算/渠道
            # "tradeChannel": "1024",    # 清运结算/回收结算/渠道
            # "createTime": "",          # 创建时间
            # "userId": "1024",          # 用户编号
            # "userType": "1",           # 用户类型
        }

        resp = api_session.get(url, headers=auth_headers, params=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        assert r["data"]["total"] > 0
        assert len(r["data"]["list"]) > 0
        print(r)