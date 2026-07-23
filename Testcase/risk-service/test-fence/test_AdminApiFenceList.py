import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()


@pytest.mark.skip(reason="接口参数待确认")
class Test_AdminApiFenceList:
    """admin获取电子围栏列表"""

    @pytest.mark.smoke
    def test_AdminApiFenceList(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/risk/electronic-fence/list"
        params = {"pageNo": 1, "pageSize": 10}
        ok(api_session.get(url, params=params, headers=auth_headers))
