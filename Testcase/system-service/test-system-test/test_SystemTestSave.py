import pytest
from config import ADMIN_URL


class TestSystemTestSave:
    """保存测试数据（用于分布式事务测试）"""

    @pytest.mark.smoke
    def test_SystemTestSave(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/test/save"
        body = {
            "name":"autotest",
            "age":19
                }  # TODO: 补充参数
        ok(api_session.post(url, json=body, headers=auth_headers))
        r = resp.json()
        #assert r["code"] == 0
        print(r)
