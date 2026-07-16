import pytest
from config import ADMIN_URL


class TestCrmContractSubmit:
    """提交合同审批"""

    @pytest.mark.smoke
    def test_CrmContractSubmit(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/contract/submit"
        body = {
            "id": 1,  # TODO: 补充参数
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
