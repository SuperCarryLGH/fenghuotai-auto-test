import pytest
from config import ADMIN_URL


class TestBpmProcessInstanceGetApprovalDetail:
    """获得审批详情"""

    @pytest.mark.smoke
    def test_BpmProcessInstanceGetApprovalDetail(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/bpm/process-instance/get-approval-detail"
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
