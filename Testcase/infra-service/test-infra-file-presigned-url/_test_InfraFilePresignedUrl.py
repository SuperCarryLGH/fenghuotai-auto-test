import pytest
from config import APP_URL


class TestInfraFilePresignedUrl:
    """获取文件预签名地址（上传）"""

    @pytest.mark.smoke
    def test_InfraFilePresignedUrl(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/infra/file/presigned-url"
        # 文件上传接口，需构造 multipart/form-data
                body = {
            # TODO: 补充创建参数
        }
        resp = api_session.post(url, json=body, headers=auth_headers)
