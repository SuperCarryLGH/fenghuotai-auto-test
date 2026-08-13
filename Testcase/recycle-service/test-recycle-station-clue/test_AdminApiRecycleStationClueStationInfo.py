import pytest
from config import ADMIN_URL


class Test_AdminApiRecycleStationClueStationInfo:
    """线索站点信息"""

    @pytest.mark.smoke
    @pytest.mark.skip(reason="线索/签约业务流字段契约未完全确认(网点ID/拜访意向/运行状态等)，待补")
    def test_AdminApiRecycleStationClueStationInfo(self, clue_chain, api_session, ok):
        chain, clue_id, clue_no, auth_headers = clue_chain
        url = f"{ADMIN_URL}/admin-api/recycle/station-clue/station-info"
        r = ok(api_session.get(url, params={"id": clue_id}, headers=auth_headers))
        print(r)
