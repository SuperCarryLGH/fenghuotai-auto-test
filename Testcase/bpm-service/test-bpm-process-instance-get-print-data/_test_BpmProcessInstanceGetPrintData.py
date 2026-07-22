import pytest
from config import ADMIN_URL


class TestBpmProcessInstanceGetPrintData:
    """获得流程实例的打印数据"""

    @pytest.mark.smoke
    def test_BpmProcessInstanceGetPrintData(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/bpm/process-instance/get-print-data"
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
