import pytest
from config import ADMIN_URL


class TestCrmFollowUpRecordPage:
    """获得跟进记录分页"""

    @pytest.mark.smoke
    def test_CrmFollowUpRecordPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/follow-up-record/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
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
