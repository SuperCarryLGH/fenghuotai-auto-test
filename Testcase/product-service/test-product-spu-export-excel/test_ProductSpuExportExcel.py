import pytest
from config import ADMIN_URL


class TestProductSpuExportExcel:
    """导出商品"""

    @pytest.mark.smoke
    def test_ProductSpuExportExcel(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/product/spu/export-excel"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200 and len(resp.content) > 0
        print(f"下载成功, 文件大小={len(resp.content)}bytes")
