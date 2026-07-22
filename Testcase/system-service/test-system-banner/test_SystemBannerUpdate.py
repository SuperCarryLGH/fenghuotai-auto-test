import pytest
from config import ADMIN_URL


class TestSystemBannerUpdate:
    """更新 Banner"""

    @pytest.mark.smoke
    def test_SystemBannerUpdate(self, api_session, auth_headers, autotest_banner_id):
        url = f"{ADMIN_URL}/admin-api/system/banner/update"
        body = {"id": autotest_banner_id, "title": "autotest_updated", "linkType": "1", "openType": "10", "picUrl": "http://test.com/test.jpg", "position": "1", "platform": "web", "provider": "all", "url": "http://test.com", "browseCount": 0, "memo": "autotest", "status": "0"}
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
