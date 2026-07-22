import pytest
from config import ADMIN_URL


class TestCrmBusinessGet:
    """获得商机"""

    @pytest.mark.smoke
    def test_CrmBusinessGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/business/get"
        params = {
            "id": 1,  # TODO: 替换为实际存在的 ID
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
