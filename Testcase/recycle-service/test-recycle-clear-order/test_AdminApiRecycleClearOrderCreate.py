import time
import pytest
from config import ADMIN_URL
from Common.loader import load_recycle_clear_order

module_data = load_recycle_clear_order()


class Test_AdminApiRecycleClearOrderCreate:
    """admin创建回收清运单"""

    @pytest.fixture(autouse=True)
    def _cleanup(self, api_session, auth_headers):
        self._created_id = None
        yield
        if self._created_id is not None:
            try:
                api_session.delete(f"{ADMIN_URL}/admin-api/recycle/clear-order/delete", params={"id": self._created_id}, headers=auth_headers)
            except Exception as e:
                print(f"[cleanup] 删除失败 {self._created_id}: {e}")

    @pytest.mark.smoke
    def test_AdminApiRecycleClearOrderCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/clear-order/create"
        ts = int(time.time() * 1000)
        body = {
            "clearOrderNo": f"CO_TEST{ts}",
            "clearTarget": 2,
            "clearType": 1,
            "status": 10,
            "subStatus": 11,
            "stationId": 1,
            "stationName": "站点1",
            "operationCenterId": 2074701657159761922,
        }
        r = ok(api_session.post(url, json=body, headers=auth_headers))
        self._created_id = r["data"] if isinstance(r["data"], (int, str)) and not isinstance(r["data"], bool) else (r["data"].get("id") if isinstance(r["data"], dict) else None)
