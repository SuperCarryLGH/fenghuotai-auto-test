import time
import pytest
from config import ADMIN_URL


class Test_AdminApiRecycleStationClueUpdate:
    """线索更新"""

    @pytest.mark.smoke
    def test_AdminApiRecycleStationClueUpdate(self, clue_chain, station_user_ctx, api_session, ok):
        chain, clue_id, clue_no, b_headers = clue_chain
        _, uid, uname = station_user_ctx
        url = f"{ADMIN_URL}/admin-api/recycle/station/clue/update"
        r = ok(api_session.put(url, json={
            "id": clue_id,
            "userId": uid, "userName": uname,
            "receiveUserId": uid, "receiveUserName": uname,
            "clueNo": clue_no,
            "clueName": f"autotest_clue_update_{int(time.time())}",
            "stationType": 1,
            "poolType": 0, "status": 20, "visitCount": 0,
            "provinceCode": "330000", "province": "浙江省",
            "cityCode": "330100", "city": "杭州市",
            "districtCode": "330108", "district": "滨江区",
            "detailAddress": "测试地址",
        }, headers=b_headers))
        print(r)
