import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_clear_order

common = load_common()
module_data = load_recycle_clear_order()


class Test_AdminApiRecycleClearOrderCreate:
    """admin创建回收清运单"""

    @pytest.mark.smoke
    def test_AdminApiRecycleClearOrderCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/clear-order/create"
        suffix = str(int(time.time()))
        body = {
            "name": f"{module_data['clear_order']['name']}_{suffix}",
            "status": common['common']['status']['enabled'],
        }
        ok(api_session.post(url, json=body, headers=auth_headers))
