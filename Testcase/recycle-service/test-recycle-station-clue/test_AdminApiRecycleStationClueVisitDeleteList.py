import time
import pytest
from pygments.lexers import data

from config import ADMIN_URL


class Test_AdminApiRecycleStationClueVisitDeleteList:
    """admin批量删除网点线索拜访记录"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationClueVisitDeleteList(self, clue_chain, station_user_ctx, api_session, ok):
        chain, clue_id, clue_no, b_headers = clue_chain
        _, uid, uname = station_user_ctx
        r = ok(api_session.post(f"{ADMIN_URL}/admin-api/recycle/station/clue-visit/create", json={
            "clueId": clue_id,
            "clueNo": clue_no,
            "userId": uid, "userName": uname,
            "visitTime": time.strftime("%Y-%m-%d %H:%M:%S"),
            "visitIntention": 1,
        }, headers=b_headers))
        visit_id = r["data"] if isinstance(r["data"], (int, str)) and not isinstance(r["data"], bool) else (r["data"].get("id") if isinstance(r["data"], dict) else None)
        url = f"{ADMIN_URL}/admin-api/recycle/station/clue-visit/delete-list"
        resp = api_session.delete(url, params={"ids": [visit_id]}, headers=b_headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        print(f"{data}批量删除成功")
