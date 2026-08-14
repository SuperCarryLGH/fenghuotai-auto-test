import pytest
from Common.DB import query

class Test_AppApiMemberAppContractCreate:
    """创建签约合同"""
    @pytest.mark.smoke
    def test_AppContractCreate(self,autotest_contract_create):
        contract_id = autotest_contract_create
        assert contract_id,"合同创建失败"
        resp = query("SELECT id,contract_no from member_contract where contract_no = %s",(contract_id,))
        assert resp, f"数据库未查到合同 contract_no={contract_id}"
        print("合同创建成功，contract_no= %s,db_id= %s"%(contract_id,resp[0]['id']))
