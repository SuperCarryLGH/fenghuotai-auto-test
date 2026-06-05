import pytest
from config import ADMIN_URL
from Common.loader import load_station
station = load_station()

class TestAppApiRecycleBannerGetByPositions:
    """用户 APP - 根据位置获取banner"""

    def test_AppApiRecycleBannerGetByPositions(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/app-api/recycle/banner/get-by-positions"
        params = {
                    "position": 1,
            }

        resp = api_session.get(url, headers=auth_headers,params=params)
        #assert resp.status_code == 200
        data = resp.json()
        #assert data["code"] == 0
        #assert data["data"] == {}
        print(data)