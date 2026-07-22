import pytest
from config import ADMIN_URL
class Test_AdminApiRecycleAmapPageCommunitys:
    """admin更新回收站点签约"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAmapPageCommunitys(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/amap/pageCommunitys"
        body = {
            "region": '116.310003', #经度
            "pageNo": '39.991957', #纬度
            "pageSize": '', #返回结果控制：base-基本地址，all-含 POI/道路等,示例值(base)
            "keywords":'',#搜索半径（米），extensions=all 时生效，范围 0~3000,示例值(1000)
            "types":'',
            "cityLimit":''
        }
        resp = api_session.get(url, params=body, headers=auth_headers)
        assert resp.status_code == 200
