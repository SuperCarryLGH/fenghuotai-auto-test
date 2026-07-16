import pytest
from config import ADMIN_URL


class TestBpmTaskManagerPage:
    """获取全部任务的分页"""

    @pytest.mark.smoke
    def test_BpmTaskManagerPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/bpm/task/manager-page"
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
