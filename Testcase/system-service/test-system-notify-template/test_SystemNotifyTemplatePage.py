import pytest
from config import ADMIN_URL


class TestSystemNotifyTemplatePage:
    """获得站内信模版分页"""

    @pytest.mark.smoke
    def test_SystemNotifyTemplatePage(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/system/notify-template/page"
        params = {
            "pageNo": 1,
            "pageSize": 10,
        }
        ok(api_session.get(url, params=params, headers=auth_headers))
        r = resp.json()
        assert r["code"] == 0
        print(r)
