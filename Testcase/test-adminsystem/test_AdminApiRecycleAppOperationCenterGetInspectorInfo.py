import pytest
from config import ADMIN_URL
from Common.loader import load_dept
#dept = load_dept()

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
        data = resp.json()
        assert data["code"] == 0
        #assert data["data"] == "河南省 郑州市"
        print(data)




#test_AdminApiSystemAreaGetByIp








#AdminApiRecycleAppOperationCenterGetInspectorInfo