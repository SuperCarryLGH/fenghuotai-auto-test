import pytest
from config import APP_URL
from Common.loader import load_station
station = load_station()

class TestAppApiRecycleStationDetail:
    """用户 APP - 站点全量详情（基础信息+签约配置完整数据）"""

    @pytest.mark.smoke
    def test_AppApiRecycleStationDetail(self, api_session, auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{APP_URL}/app-api/recycle/station/detail"
        params = {
                    "id": station["station"]["id"],
            }

        resp = api_session.get(url, headers=auth_headers, params=params)
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        #assert data["data"] == {}
        print(data)