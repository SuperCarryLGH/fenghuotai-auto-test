import time
import pytest
from config import ADMIN_URL


class Test_AdminApiRecycleStationClueVisitUpdate:
    """admin更新网点线索拜访记录"""

    @pytest.fixture(autouse=True)
    def _cleanup(self):
        self._created_id = None
        yield
        if self._created_id is not None and getattr(self, "_b_headers", None):
            try:
                api_session = self._api_session
                api_session.delete(f"{ADMIN_URL}/admin-api/recycle/station/clue-visit/delete",
                                   params={"id": self._created_id}, headers=self._b_headers)
            except Exception as e:
                print(f"[cleanup] 删除失败 {self._created_id}: {e}")

    @pytest.mark.smoke
    def test_AdminApiRecycleStationClueVisitUpdate(self, clue_chain, station_user_ctx, api_session, ok):
        self._api_session = api_session
        chain, clue_id, clue_no, b_headers = clue_chain
        self._b_headers = b_headers
        _, uid, uname = station_user_ctx
        r = ok(api_session.post(f"{ADMIN_URL}/admin-api/recycle/station/clue-visit/create", json={
            "clueId": clue_id,
            "clueNo": clue_no,
            "userId": uid, "userName": uname,
            "visitTime": time.strftime("%Y-%m-%d %H:%M:%S"),
            "visitIntention": 1,
        }, headers=b_headers))
        self._created_id = r["data"] if isinstance(r["data"], (int, str)) and not isinstance(r["data"], bool) else (r["data"].get("id") if isinstance(r["data"], dict) else None)
        url = f"{ADMIN_URL}/admin-api/recycle/station/clue-visit/update"
        ok(api_session.put(url, json={
            "id": self._created_id,
            "clueId": clue_id,
            "clueNo": clue_no,
            "userId": uid, "userName": uname,
            "visitTime": time.strftime("%Y-%m-%d %H:%M:%S"),
            "visitIntention": 2,
        }, headers=b_headers))
