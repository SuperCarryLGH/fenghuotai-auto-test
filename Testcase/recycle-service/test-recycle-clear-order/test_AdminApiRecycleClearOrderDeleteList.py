import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_clear_order

common = load_common()
module_data = load_recycle_clear_order()


class Test_AdminApiRecycleClearOrderDeleteList:
    """admin批量删除回收清运单"""

    @pytest.mark.smoke
    def test_AdminApiRecycleClearOrderDeleteList(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/clear-order/delete-list"
        params = {"ids": [common['common']['id']['invalid']]}
        ok(api_session.delete(url, params=params, headers=auth_headers))
