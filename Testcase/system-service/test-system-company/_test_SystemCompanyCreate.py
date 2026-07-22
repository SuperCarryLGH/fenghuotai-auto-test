import pytest
from config import ADMIN_URL


class TestSystemCompanyCreate:
    """创建公司"""

    @pytest.mark.smoke
    def test_SystemCompanyCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/company/create"
        import time
        suffix = str(int(time.time() * 1000))[-10:]
        body = {"name": f"测试公司_{suffix}", "companyId": f"cmp_{suffix}", "fundPurpose": 2, "remark": "autotest", "status": 0, "payKey": f"company_{suffix}"}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
