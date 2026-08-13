import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_system_company

common = load_common()
company_data = load_system_company()


class Test_AdminApiSystemCompanyCreate:
    """创建公司"""

    @pytest.fixture(autouse=True)
    def _cleanup(self, api_session, auth_headers):
        self._created_id = None
        yield
        if self._created_id is not None:
            try:
                api_session.delete(f"{ADMIN_URL}/admin-api/system/company/delete", params={"id": self._created_id}, headers=auth_headers)
            except Exception as e:
                print(f"[cleanup] 删除失败 {self._created_id}: {e}")


    @pytest.mark.smoke
    @pytest.mark.skip(reason="公司创建需关联登录账号，业务逻辑未确认")
    def test_AdminApiSystemCompanyCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/company/create"
        suffix = str(int(time.time()))
        body = {
            "name": f"{company_data['company']['name']}_{suffix}",
            "fundPurpose": 1,
            "status": 0,
        }
        r = ok(api_session.post(url, json=body, headers=auth_headers))
        self._created_id = r["data"] if isinstance(r["data"], (int, str)) and not isinstance(r["data"], bool) else (r["data"].get("id") if isinstance(r["data"], dict) else None)
