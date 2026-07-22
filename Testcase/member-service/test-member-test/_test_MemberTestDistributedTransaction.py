import pytest
from config import ADMIN_URL


class TestMemberTestDistributedTransaction:
    """测试分布式事务（同时操作 member、recycle、system 三个模块）"""

    @pytest.mark.smoke
    def test_MemberTestDistributedTransaction(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/member/test/distributed-transaction"
        body = {"id": 1}  # TODO: 补充参数
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
