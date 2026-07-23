import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


class Test_AdminApiRecycleAppOperationCenterInspectOnePackage:
    """admin验货单个包裹"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAppOperationCenterInspectOnePackage(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/recycle/app-operation-center/inspect-one-package"
        body = {"id": 1}
        ok(api_session.post(url, json=body, headers=auth_headers))
