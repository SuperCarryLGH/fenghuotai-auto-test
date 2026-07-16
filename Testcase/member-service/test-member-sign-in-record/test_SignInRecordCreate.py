import pytest
from config import APP_URL


class TestSignInRecordCreate:
    """签到"""

    @pytest.mark.smoke
    def test_SignInRecordCreate(self, api_session, auth_headers):
        url = f"{APP_URL}/app-api/member/sign-in/record/create"
        body = {"name": f"签到_194200", "point": 10, "status": 0}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
