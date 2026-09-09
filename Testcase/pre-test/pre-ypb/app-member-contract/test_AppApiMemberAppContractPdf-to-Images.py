import pytest


from config import APP_URL



class TestAppApiMemberAppContractPdf:
    @pytest.mark.smoke
    def test_ConstactPdf(self,api_session,auth_headers):
        body={
            "contract_type": 1,
        }
        resp = api_session.post(f"{APP_URL}/app-api/member/app/contract/pdf-to-images",body=body,headers=auth_headers)
        assert resp.status_code == 200
        data=resp.json()
        assert data["data"] is None,f"合同模版上传失败：{data['data']['msg']}"
        print(f"合同模版上传成功")
    