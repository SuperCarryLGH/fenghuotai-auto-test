import time
import pytest
from config import ADMIN_URL


class Test_AdminApiRecycleStationSignUpdate:
    """admin更新回收站点签约"""

    @pytest.fixture(autouse=True)
    def _cleanup(self):
        self._created_id = None
        yield
        if self._created_id is not None and getattr(self, "_b_headers", None):
            try:
                self._api_session.delete(f"{ADMIN_URL}/admin-api/recycle/station/sign/delete", params={"id": self._created_id}, headers=self._b_headers)
            except Exception as e:
                print(f"[cleanup] 删除失败 {self._created_id}: {e}")

    @pytest.mark.smoke
    def test_AdminApiRecycleStationSignUpdate(self, clue_chain, station_user_ctx, api_session, ok):
        self._api_session = api_session
        chain, clue_id, clue_no, b_headers = clue_chain
        self._b_headers = b_headers
        _, uid, uname = station_user_ctx
        # 先建一个签约，再更新
        r = ok(api_session.post(f"{ADMIN_URL}/admin-api/recycle/station/sign/create", json={
            "signNo": f"SIGN_{int(time.time() * 1000)}",
            "clueId": clue_id,
            "clueNo": clue_no,
            "userId": str(uid), "userName": uname,
            "signStatus": 10, "status": 1,
        }, headers=b_headers))
        sign_id = r["data"] if isinstance(r["data"], (int, str)) and not isinstance(r["data"], bool) else (r["data"].get("id") if isinstance(r["data"], dict) else None)
        self._created_id = sign_id
        url = f"{ADMIN_URL}/admin-api/recycle/station/sign/update"
        ok(api_session.put(url, json={
            "id": sign_id,
            "signNo": f"SIGN_{int(time.time() * 1000)}_U",
            "clueId": clue_id,
            "clueNo": clue_no,
            "userId": str(uid), "userName": "autotest_update",
            "signStatus": 10, "status": 1,
        }, headers=b_headers))
