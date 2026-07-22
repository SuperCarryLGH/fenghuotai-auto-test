import pytest
from config import ADMIN_URL


class TestCrmBusinessUpdateStatus:
    """更新商机状态"""

    @pytest.mark.smoke
    def test_CrmBusinessUpdateStatus(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/business/update-status"
        body = {
            "ids": [],  # TODO: 批量操作的 ID 列表
            "status": 0,  # TODO: 确认状态值
        }
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)

 == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
