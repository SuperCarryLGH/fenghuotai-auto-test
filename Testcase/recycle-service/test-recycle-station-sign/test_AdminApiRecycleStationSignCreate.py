import time
import pytest
from config import ADMIN_URL


class Test_AdminApiRecycleStationSignCreate:
    """admin创建回收站点签约"""

    @pytest.fixture(autouse=True)
    def _cleanup(self, api_session, auth_headers):
        self._created_id = None
        yield
        if self._created_id is not None:
            try:
                api_session.delete(f"{ADMIN_URL}/admin-api/recycle/station/sign/delete", params={"id": self._created_id}, headers=auth_headers)
            except Exception as e:
                print(f"[cleanup] 删除失败 {self._created_id}: {e}")

    @pytest.mark.smoke
    @pytest.mark.skip(reason="线索/签约业务流字段契约未完全确认(网点ID/拜访意向/运行状态等)，待补")
    def test_AdminApiRecycleStationSignCreate(self, clue_chain, api_session, ok):
        chain, clue_id, clue_no, auth_headers = clue_chain
        url = f"{ADMIN_URL}/admin-api/recycle/station/sign/create"
        body = {
            "signNo": f"SIGN_{int(time.time() * 1000)}",
            "clueId": clue_id,
            "clueNo": clue_no,
            "userName": "autotest",
        }
        r = ok(api_session.post(url, json=body, headers=auth_headers))
        self._created_id = r["data"] if isinstance(r["data"], (int, str)) and not isinstance(r["data"], bool) else (r["data"].get("id") if isinstance(r["data"], dict) else None)
