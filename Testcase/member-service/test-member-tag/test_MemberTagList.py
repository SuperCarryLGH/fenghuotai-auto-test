import pytest
from config import ADMIN_URL


class TestMemberTagList:
    """获得会员标签列表"""

    @pytest.mark.smoke
    def test_MemberTagList(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/member/tag/list"
        params = {"ids": "1,2"}  # 查询绿色和黄色两个已存在的标签
        r = ok(api_session.get(url, params=params, headers=auth_headers))
