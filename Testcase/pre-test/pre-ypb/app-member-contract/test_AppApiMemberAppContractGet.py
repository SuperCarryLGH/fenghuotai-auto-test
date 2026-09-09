import pytest
from config import APP_URL
class TestAppApiMemberAppContractGet:
    @pytest.mark.smoke
    def test_ContractGet(self,autotest_contract_create,api_session, auth_headers):
        contract_id = autotest_contract_create
        params = {
            "id":contract_id,
        }
        resp = api_session.get(f"{APP_URL}/app-api/member/app/contract/get",params=params,headers=auth_headers)
        assert resp.status_code == 200
        data=resp.json()
        assert data["data"]["id"] == contract_id
        print(f"合同信息获取成功，合同信息: {data['data']}")