import pytest
from config import APP_URL
from Common.loader import load_station
station = load_station()

class TestAppApiRecycleBannerGetByPosition:
    """用户 APP - 根据位置获取banner"""

    @pytest.mark.smoke
    def test_AppApiRecycleBannerGetByPosition(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{APP_URL}/app-api/recycle/banner/get-by-position"
        params = {
                    "position": 1,
            }

        resp = api_session.get(url, headers=auth_headers,params=params)
        #assert resp.status_code == 200
        data = resp.json()
        #assert data["code"] == 0
        #assert data["data"] == {}
        print(data)