import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_clear_order

common = load_common()
module_data = load_recycle_clear_order()


class Test_AdminApiRecycleClearOrderGet:
    """admin获取回收清运单详情"""

    @pytest.mark.smoke
    def test_AdminApiRecycleClearOrderGet(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/clear-order/get"
        params = {"id": module_data['clear_order']['id']}
        ok(api_session.get(url, params=params, headers=auth_headers))
