import time
import pytest
from config import ADMIN_URL


class Test_AdminApiRecycleStationClueUpdate:
    """线索更新"""

    @pytest.mark.smoke
    @pytest.mark.skip(reason="线索/签约业务流字段契约未完全确认(网点ID/拜访意向/运行状态等)，待补")
    def test_AdminApiRecycleStationClueUpdate(self, clue_chain, api_session, ok):
        chain, clue_id, clue_no, auth_headers = clue_chain
        url = f"{ADMIN_URL}/admin-api/recycle/station/clue/update"
        r = ok(api_session.put(url, json={
            "id": clue_id,
            "clueName": f"autotest_clue_update_{int(time.time())}",
            "stationType": 1,
            "provinceCode": "330000", "province": "浙江省",
            "cityCode": "330100", "city": "杭州市",
            "districtCode": "330108", "district": "滨江区",
            "detailAddress": "测试地址",
        }, headers=auth_headers))
        print(r)
