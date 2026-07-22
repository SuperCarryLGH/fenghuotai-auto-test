import pytest
from config import ADMIN_URL


class TestProcessInstanceCopyPage:
    """获得抄送流程分页列表"""

    @pytest.mark.smoke
    def test_ProcessInstanceCopyPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/bpm/process-instance/copy/page"
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
