import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiRecycleAppOperationCenterInspectOnePackage:
    """admin验货单个包裹"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAppOperationCenterInspectOnePackage(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/app-operation-center/inspect-one-package"
        body = {"id": common['common']['id']['valid']}
        resp = api_session.post(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
