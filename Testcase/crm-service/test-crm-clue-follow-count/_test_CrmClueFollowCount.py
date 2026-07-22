import pytest
from config import ADMIN_URL


class TestCrmClueFollowCount:
    """获得分配给我的、待跟进的线索数量"""

    @pytest.mark.smoke
    def test_CrmClueFollowCount(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/clue/follow-count"
        params = {
            # TODO: 补充查询参数
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)

 == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
