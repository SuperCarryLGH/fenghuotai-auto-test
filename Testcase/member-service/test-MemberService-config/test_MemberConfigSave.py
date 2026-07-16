import pytest
from config import ADMIN_URL


class TestMemberConfigSave:
    """保存会员配置"""

    @pytest.mark.smoke
    def test_MemberConfigSave(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/member/config/save"
        params = {
            "pointTradeDeductEnable": "true", #积分抵扣开关
            "pointTradeDeductUnitPrice": "13506", #积分抵扣
            "pointTradeDeductMaxPrice": "32428", #积分抵扣最大值
            "pointTradeGivePoint": "100", # 1元赠送多少分
            }

        resp = api_session.put(url, headers=auth_headers,json=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] == {}
        print(r)








#test_AppApiCooperationGetByPlatform