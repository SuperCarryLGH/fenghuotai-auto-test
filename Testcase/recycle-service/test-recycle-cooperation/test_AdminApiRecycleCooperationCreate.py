import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_recycle_cooperation

common = load_common()
module_data = load_recycle_cooperation()


class Test_AdminApiRecycleCooperationCreate:
    """admin创建回收合作方"""

    @pytest.mark.smoke
    def test_AdminApiRecycleCooperationCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/station/cooperation/create"
        suffix = str(int(time.time()))
        body = {"name": f"{module_data['cooperation']['name']}_{suffix}", "status": common['common']['status']['enabled']}
        ok(api_session.post(url, json=body, headers=auth_headers))
