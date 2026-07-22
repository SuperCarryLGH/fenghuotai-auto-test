import pytest
from config import ADMIN_URL


class TestOaLeaveCreate:
    """创建请求申请"""

    @pytest.mark.smoke
    def test_OaLeaveCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/bpm/oa/leave/create"
        body = {
            # TODO: 补充创建参数
            # 示例: "name": f"autotest_182356", "status": 0,
        }
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)

 == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
