import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiRecycleAppOperationCenterOnePackageDetail:
    """admin单个包裹详情"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAppOperationCenterOnePackageDetail(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/recycle/app-operation-center/one-package-detail"
        params = {"id": common['common']['id']['valid']}
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
