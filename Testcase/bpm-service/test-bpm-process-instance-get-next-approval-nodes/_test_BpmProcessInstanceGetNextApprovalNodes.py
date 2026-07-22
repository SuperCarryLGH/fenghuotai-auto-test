import pytest
from config import ADMIN_URL


class TestBpmProcessInstanceGetNextApprovalNodes:
    """获取下一个执行的流程节点"""

    @pytest.mark.smoke
    def test_BpmProcessInstanceGetNextApprovalNodes(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/bpm/process-instance/get-next-approval-nodes"
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
