import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_station_map

common = load_common()
module_data = load_recycle_station_map()


class Test_AdminApiRecycleStationMapCreate:
    """admin创建回收站点地图"""

    @pytest.fixture(autouse=True)
    def _cleanup(self, api_session, auth_headers):
        self._created_id = None
        yield
        if self._created_id is not None:
            try:
                api_session.delete(f"{ADMIN_URL}/admin-api/recycle/station/map/delete", params={"id": self._created_id}, headers=auth_headers)
            except Exception as e:
                print(f"[cleanup] 删除失败 {self._created_id}: {e}")


    @pytest.mark.smoke
    def test_AdminApiRecycleStationMapCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/station/map/create"
        suffix = str(int(time.time()))
        body = {"name": f"{module_data['station_map']['name']}_{suffix}", "status": common['common']['status']['enabled']}
        r = ok(api_session.post(url, json=body, headers=auth_headers))
        self._created_id = r["data"] if isinstance(r["data"], (int, str)) and not isinstance(r["data"], bool) else (r["data"].get("id") if isinstance(r["data"], dict) else None)
