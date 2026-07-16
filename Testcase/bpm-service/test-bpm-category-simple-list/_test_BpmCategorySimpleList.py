import pytest
from config import ADMIN_URL


class TestBpmCategorySimpleList:
    """获取流程分类的精简信息列表"""

    @pytest.mark.smoke
    def test_BpmCategorySimpleList(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/bpm/category/simple-list"
                params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
