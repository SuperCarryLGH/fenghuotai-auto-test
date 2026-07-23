import pytest
from config import ADMIN_URL
class Test_AdminApiRecycleAmapPageCommunitys:
    """admin更新回收站点签约"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAmapPageCommunitys(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/amap/pageCommunitys"
        body = {
            "region": "杭州",
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=body, headers=auth_headers))
