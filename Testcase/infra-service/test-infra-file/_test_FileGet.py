import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class TestFileGet:
    """文件访问（{configId} 替换为具体文件配置ID）"""

    @pytest.mark.smoke
    def test_FileGet(self, api_session, auth_headers):
        config_id = common["common"]["id"]["valid"]
        # {path} 替换为具体文件路径
        url = f"{ADMIN_URL}/admin-api/infra/file/{config_id}/get/test.jpg"
        params = {
            # TODO: 补充查询参数
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)

 == 200
        # 文件接口可能返回二进制，不做 JSON 解析
