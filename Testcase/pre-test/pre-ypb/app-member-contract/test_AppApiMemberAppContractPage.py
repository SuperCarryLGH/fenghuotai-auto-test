import pytest
from config import APP_URL
from Common.loader import load_page
class TestAppApiMemberAppContractPage:
    @pytest.mark.smoke
    def test_ContractPage(self,api_session,auth_headers):
        page = load_page()
        body={
            "pageNo":page["page"]["pageNo"],
            "pageSize":page["page"]["pageSize"],
        }
        resp = api_session.get(f"{APP_URL}/app-api/member/app/contract/page",headers=auth_headers,params=body)
        assert resp.status_code == 200
        data=resp.json()
        assert data["data"]["total"]>0,f"当前用户合同记录为空"
        print(f"当前合同信息为:{data['data']['list']}")