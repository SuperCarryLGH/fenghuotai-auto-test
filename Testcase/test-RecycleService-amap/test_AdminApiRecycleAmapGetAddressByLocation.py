import pytest
from config import ADMIN_URL
class Test_AdminApiRecycleAmapGetAddressByLocation:
    """admin更新回收站点签约"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAmapGetAddressByLocation(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/amap/getAddressByLocation"
        body = {
            "longitude": '116.310003', #经度
            "latitude": '39.991957', #纬度
            "extensions": '', #返回结果控制：base-基本地址，all-含 POI/道路等,示例值(base)
            "radius":'' #搜索半径（米），extensions=all 时生效，范围 0~3000,示例值(1000)
        }
        resp = api_session.get(url, params=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
