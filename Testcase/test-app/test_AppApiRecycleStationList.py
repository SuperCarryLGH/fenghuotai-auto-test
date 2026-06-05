import pytest
from config import APP_URL
from Common.loader import load_station, load_page, load_common
station = load_station()
page = load_page()
common = load_common()

class TestAppApiRecycleStationList:
    """用户 APP - 根据类型查询站点列表（分页精简）"""

    @pytest.mark.smoke
    def test_AppApiRecycleStationList(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{APP_URL}/app-api/recycle/station/list"
        params = {
            "type": station["station"]["type"],
            "pageNo": common['common']['page']['pageNo'],
            "pageSize": common['common']['page']['pageSize'],
            }

        resp = api_session.get(url, headers=auth_headers,params=params)
        #assert resp.status_code == 200
        r = resp.json()
        #assert r["code"] == 0
        #assert r["data"] == {}
        print(r)