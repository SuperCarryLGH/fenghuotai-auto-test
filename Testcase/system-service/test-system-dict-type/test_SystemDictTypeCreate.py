import pytest
from config import ADMIN_URL


class TestSystemDictTypeCreate:
    """创建字典类型"""

    @pytest.mark.smoke
    def test_SystemDictTypeCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/dict-type/create"
        import time
        body = {"name": f"测试字典_{int(time.time())}", "type": f"test_type_{int(time.time())}", "status": 0}
        ok(api_session.post(url, json=body, headers=auth_headers))
