import pytest
from config import ADMIN_URL


class TestBpmTaskDonePage:
    """获取 Done 已办任务分页"""

    @pytest.mark.smoke
    def test_BpmTaskDonePage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/bpm/task/done-page"
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
