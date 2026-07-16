import pytest
from config import APP_URL


class TestInfraFileUpload:
    """上传文件"""

    @pytest.mark.smoke
    def test_InfraFileUpload(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/infra/file/upload"
        # 文件上传接口，需构造 multipart/form-data
                body = {
            # TODO: 补充创建参数
        }
        resp = api_session.post(url, json=body, headers=auth_headers)
