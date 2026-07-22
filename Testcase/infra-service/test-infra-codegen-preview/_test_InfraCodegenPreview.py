import pytest
from config import ADMIN_URL


class TestInfraCodegenPreview:
    """预览生成代码"""

    @pytest.mark.smoke
    def test_InfraCodegenPreview(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/infra/codegen/preview"
                params = {}
        resp = api_session.get(url, params=params, headers=auth_headers)
