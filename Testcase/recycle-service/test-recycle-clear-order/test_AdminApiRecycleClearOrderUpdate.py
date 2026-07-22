import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_clear_order

common = load_common()
module_data = load_recycle_clear_order()


class Test_AdminApiRecycleClearOrderUpdate:
    """admin更新回收清运单"""

    @pytest.mark.smoke
    def test_AdminApiRecycleClearOrderUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/clear-order/update"
        suffix = str(int(time.time()))
        body = {
            "id": common['common']['id']['valid'],
            "name": f"{module_data['clear_order']['update_name']}_{suffix}",
            "status": common['common']['status']['enabled'],
        }
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
