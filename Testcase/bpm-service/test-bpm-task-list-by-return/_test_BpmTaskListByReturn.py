import pytest
from config import ADMIN_URL


class TestBpmTaskListByReturn:
    """获取所有可退回的节点"""

    @pytest.mark.smoke
    def test_BpmTaskListByReturn(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/bpm/task/list-by-return"
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
