import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_admin_order

common = load_common()
module_data = load_recycle_admin_order()


class Test_AdminApiRecycleAdminOrderExportExcel:
    """admin导出回收订单Excel"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAdminOrderExportExcel(self, api_session, auth_headers, tmp_path):
        """使用 tmp_path 自动清理"""
        url = f"{ADMIN_URL}/admin-api/recycle/admin-order/export-excel"
        params = {
            "pageNo": common['common']['page']['pageNo'],
            "pageSize": common['common']['page']['pageSize'],
        }
        resp = api_session.get(url, params=params, headers=auth_headers)

        assert resp.status_code == 200
        assert len(resp.content) > 0
        assert resp.content[:2] == b'PK', "返回内容不是有效的 Excel 文件"

        # 保存到临时目录（测试结束后自动删除）
        filename = f"recycle_order_export_{int(time.time())}.xlsx"
        file_path = tmp_path / filename

        with open(file_path, 'wb') as f:
            f.write(resp.content)

        print(f"✅ Excel 文件已保存: {file_path}")
        print(f"📁 文件大小: {len(resp.content)} bytes")
        print(f"📂 临时目录: {tmp_path}")