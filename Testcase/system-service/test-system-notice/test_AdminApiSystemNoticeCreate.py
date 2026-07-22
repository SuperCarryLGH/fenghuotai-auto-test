import time
import pytest
from config import ADMIN_URL
from Common.loader import load_common, load_system_notice

common = load_common()
notice_data = load_system_notice()


class Test_AdminApiSystemNoticeCreate:
    """创建通知公告"""

    @pytest.mark.smoke
    def test_AdminApiSystemNoticeCreate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/system/notice/create"
        suffix = str(int(time.time()))
        body = {
            "title": f"{notice_data['notice']['name']}_{suffix}",
            "content": f"测试公告内容_{suffix}",
            "status": common['common']['status']['enabled'],
        }
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
