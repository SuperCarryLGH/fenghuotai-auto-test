import pytest
from config import ADMIN_URL


class TestCrmContactDeleteBusinessList2:
    """删除联系人与联系人的关联"""

    @pytest.mark.smoke
    def test_CrmContactDeleteBusinessList2(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/contact/delete-business-list2"
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
