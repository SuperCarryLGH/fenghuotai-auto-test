import pytest
from config import ADMIN_URL
from Common.loader import load_page
page = load_page()

class Test_AdminApiRecycleAppOperationCenterGetOperationCenterRecycleClean:
    """获取IP对应的地区名"""

    @pytest.mark.smoke
    def test_AdminApiRecycleAppOperationCenterGetOperationCenterRecycleClean(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/recycle/app-operation-center/get-operation-center-recycle-clean"
        params = {
            "pageNo":page["page"]["pageNo"],
            "pageSize":page["page"]["pageSize"],

            }

        resp = api_session.get(url, headers=auth_headers,params=params)
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        #assert data["data"] == "河南省 郑州市"
        print(data)
