from xxlimited import Null

import pytest
from config import ADMIN_URL
class TestAdminApiPayWalletPage:
    """获得钱包分页（按 walletType 区分持有人）"""

    @pytest.mark.smoke
    def test_AdminApiPayWalletPage(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/pay/wallet/page"
        params = {
            "walletType": "40",  # [必填] 钱包类型 10-分拣中心 20-前置仓 30-站点 40-用户
            "pageNo": 1,  # [必填] 页码，从1开始
            "pageSize": 10,  # [必填] 每页条数，最大200
            # "userId": "1024",          # 用户编号（walletType=40时使用）
            # "stationIdName": "1560",   # 分拣中心ID或者名称
            # "userType": "1",           # 用户类型
            # "bizType": "10",           # 业务类型 10-分拣中心 20-前置仓 30-站点 40-用户
            # "createTime": "",          # 创建时间
            # "stationId": "1560",       # 站点ID（walletType=30时使用）
            # "companyId": "1560",       # 所属公司ID
            # "mobile": "1560",          # 负责人手机号/用户手机号
        }

        resp = api_session.get(url, headers=auth_headers,params=params)
        assert resp.status_code == 200
        r = resp.json()
        max=r["data"]["total"]-1
        assert r["code"] == 0
        assert r["data"]["total"] != Null
        assert r["data"]["list"][max] != Null
        print(r)