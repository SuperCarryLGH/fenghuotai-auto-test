import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_system_post

common = load_common()
post_data = load_system_post()


class Test_AdminApiSystemPostCreate:
    """创建岗位"""

    @pytest.mark.smoke
    def test_AdminApiSystemPostCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/post/create"
        suffix = str(int(time.time()))
        body = {
            "name": f"{post_data['post']['name']}_{suffix}",
            "code": post_data['post']['create']['code'],
            "sort": post_data['post']['create']['sort'],
            "status": common['common']['status']['enabled'],
        }
        ok(api_session.post(url, json=body, headers=auth_headers))
