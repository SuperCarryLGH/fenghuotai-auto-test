import pytest
from config import APP_URL


class TestPromotionBargainRecordCreate:
    """创建砍价记录"""

    @pytest.mark.smoke
    def test_PromotionBargainRecordCreate(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/promotion/bargain-record/create"
        body = {"name": f"autotest_194200", "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
