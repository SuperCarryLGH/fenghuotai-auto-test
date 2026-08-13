import time
import pytest
from config import ADMIN_URL


class Test_AdminApiRecycleStationClueCreate:
    """admin创建回收站点线索"""

    @pytest.fixture(autouse=True)
    def _cleanup(self, api_session, auth_headers):
        self._created_id = None
        yield
        if self._created_id is not None:
            try:
                api_session.delete(f"{ADMIN_URL}/admin-api/recycle/station-clue/delete", params={"id": self._created_id}, headers=auth_headers)
            except Exception as e:
                print(f"[cleanup] 删除失败 {self._created_id}: {e}")

    @pytest.mark.smoke
    def test_AdminApiRecycleStationClueCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/station-clue/create"
        suffix = str(int(time.time() * 1000))
        body = {
            "poolType": 0,
            "clueName": f"autotest_clue_{suffix}",
            "stationType": 1,
            "provinceCode": "330000", "province": "浙江省",
            "cityCode": "330100", "city": "杭州市",
            "districtCode": "330108", "district": "滨江区",
            "detailAddress": "测试地址",
        }
        r = ok(api_session.post(url, json=body, headers=auth_headers))
        self._created_id = r["data"] if isinstance(r["data"], (int, str)) and not isinstance(r["data"], bool) else (r["data"].get("id") if isinstance(r["data"], dict) else None)
