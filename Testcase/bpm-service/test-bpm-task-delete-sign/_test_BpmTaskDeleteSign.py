import pytest
from config import ADMIN_URL


class TestBpmTaskDeleteSign:
    """减签"""

    @pytest.mark.smoke
    def test_BpmTaskDeleteSign(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/bpm/task/delete-sign"
        params = {
            # TODO: 补充查询参数
        }
        resp = api_session.delete(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)

 == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
