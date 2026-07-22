import pytest
from config import ADMIN_URL


class TestMemberTagList:
    """获得会员标签列表"""

    @pytest.mark.smoke
    def test_MemberTagList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/member/tag/list"
        params = {"ids": "1,2"}  # 查询绿色和黄色两个已存在的标签
        resp = api_session.get(url, params=params, headers=auth_headers)
        r = resp.json()
        print(f"LIST RESP: code={r.get('code')}, msg={r.get('msg','')}")
        assert resp.status_code == 200
        assert r["code"] == 0
        print(r)
