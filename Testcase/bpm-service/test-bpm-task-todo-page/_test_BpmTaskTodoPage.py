import pytest
from config import ADMIN_URL


class TestBpmTaskTodoPage:
    """获取 Todo 待办任务分页"""

    @pytest.mark.smoke
    def test_BpmTaskTodoPage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/bpm/task/todo-page"
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
