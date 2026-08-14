import pytest
from config import APP_URL
class TestAppApiMemberAppContractInfo:
    @pytest.mark.smoke
    def test_ContractInfo(self,api_session,auth_headers,autotest_contract_create):
        contract_id = autotest_contract_create
        resp = api_session.get(f"{APP_URL}/app-api/member/app/contract/info",headers=auth_headers)
        assert resp.status_code == 200
        data=resp.json()
        assert data["data"]["buyerContract"]["contractId"] == contract_id ,f"用户信息不匹配：contract_id={contract_id}"
        print(f"用户签约信息获取成功contract_id={contract_id}")
