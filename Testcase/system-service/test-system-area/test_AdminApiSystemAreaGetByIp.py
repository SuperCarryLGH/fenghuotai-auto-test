import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()

class Test_AdminApiSystemAreaGetByIp:
    """获得 IP 对应的地区名"""

    @pytest.mark.smoke
    def test_AdminApiSystemAreaGetByIp(self, api_session,auth_headers, ok):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/system/area/get-by-ip"
        params = {
            "ip": "123.160.230.187"
            }

        ok(api_session.get(url, headers=auth_headers,params=params))
        r = resp.json()
        assert r["code"] == 0
        assert r["data"] == "河南省 郑州市"
        print(r)
