import pytest
from config import ADMIN_URL


class TestCrmContactCreateBusinessList:
    """创建联系人与商机的关联"""

    @pytest.mark.smoke
    def test_CrmContactCreateBusinessList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/contact/create-business-list"
        body = {
            # TODO: 补充请求体参数
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
