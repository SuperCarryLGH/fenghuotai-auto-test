import pytest
from config import ADMIN_URL
from Common.loader import load_common

common = load_common()

class Test_AdminApiRecycleAppOperationCenterGetInspectorInfo:
    """获取IP对应的地区名"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAppOperationCenterGetInspectorInfo(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/recycle/app-operation-center/get-inspector-info"
        params = {

            }

        resp = api_session.get(url, headers=auth_headers,params=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] == "河南省 郑州市"
        print(r)




#test_AdminApiSystemAreaGetByIp








#AdminApiRecycleAppOperationCenterGetInspectorInfo