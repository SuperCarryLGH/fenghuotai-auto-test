import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_admin_order

common = load_common()
module_data = load_recycle_admin_order()


class Test_AdminApiRecycleAdminOrderUpdate:
    """admin更新回收订单"""

    @pytest.mark.smoke
    @pytest.mark.skip(reason="recycle 深层链路依赖仓库/订单预置数据，暂未自建")
    def test_AdminApiRecycleAdminOrderUpdate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/admin-order/update"
        body = {
            "id": module_data['admin_order']['id'],
            "orderNo": common['common']['id']['orderNo'],
            "clearStatus": common['common']['id']['clearStatus'],
            "addressId": common['common']['id']['addressId']
        }
        ok(api_session.put(url, json=body, headers=auth_headers))
