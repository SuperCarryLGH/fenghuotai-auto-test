import pytest
from config import ADMIN_URL


class TestSystemCompanyUpdate:
    """更新公司"""

    @pytest.mark.smoke
    def test_SystemCompanyUpdate(self, api_session, auth_headers, autotest_company_id):
        url = f"{ADMIN_URL}/admin-api/system/company/update"
        import time
        suffix = str(int(time.time() * 1000))[-10:]
        body = {"id": autotest_company_id, "name": "autotest_updated", "companyId": f"cmp_{suffix}", "fundPurpose": 2, "remark": "autotest", "status": 0, "payKey": f"company_{suffix}"}
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
