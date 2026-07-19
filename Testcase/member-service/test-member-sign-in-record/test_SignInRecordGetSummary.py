import pytest
from config import APP_URL


class TestSignInRecordGetSummary:
    """获得个人签到统计"""

    @pytest.mark.smoke
    def test_SignInRecordGetSummary(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/member/sign-in/record/get-summary"
        params = {"id": autotest_record_id}  # 来自 conftest fixture
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
