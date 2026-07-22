import pytest
from config import ADMIN_URL


class TestBpmFormListAllSimple:
    """获得动态表单的精简列表"""

    @pytest.mark.smoke
    def test_BpmFormListAllSimple(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/bpm/form/list-all-simple"
                params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
