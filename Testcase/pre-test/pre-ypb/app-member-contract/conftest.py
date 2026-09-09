import pytest
from config import APP_URL
from Common.DB import exec_sql


@pytest.fixture(scope="module")
def autotest_contract_create(api_session, auth_headers):
    """创建测试数据，返回 ID。模块内共享，执行完后自动清理。"""
    body = {"contractType": 1, "partyASignatureUrl": "https://example.com/signature.png"}
    resp = api_session.post(f"{APP_URL}/app-api/member/app/contract/create", json=body, headers=auth_headers)
    assert resp.status_code == 200
    data = resp.json()
    assert data["code"] == 0,f"创建签约合同失败: code={data.get('code')}, msg={data.get('msg')}"
    contract_id = data["data"]
    print(f"[Fixture] contract_create_msg = {contract_id}")
    yield contract_id
    try:
        exec_sql("DELETE from member_contract where contract_no= %s",(contract_id,))
    except Exception as e:
        print(f"[cleanup]删除失败{contract_id}:{e}")