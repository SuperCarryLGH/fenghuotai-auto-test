import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


@pytest.mark.skip(reason="接口参数待确认")
class Test_AdminApiFenceDelete:
    """admin删除电子围栏"""

    @pytest.mark.smoke
    def test_AdminApiFenceDelete(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/risk/electronic-fence/delete"
        body = {"id": common['common']['id']['invalid']}
        ok(api_session.delete(url, params=body, headers=auth_headers))
