import pytest
from config import ADMIN_URL


class TestModelSimpleGet:
    """获得仿钉钉流程设计模型"""

    @pytest.mark.smoke
    def test_ModelSimpleGet(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/bpm/model/simple/get"
                params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
