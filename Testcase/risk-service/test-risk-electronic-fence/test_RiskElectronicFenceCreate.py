import pytest
from config import ADMIN_URL


class TestRiskElectronicFenceCreate:
    """创建风控-电子围栏主"""

    @pytest.fixture(autouse=True)
    def _cleanup(self, api_session, auth_headers):
        self._created_id = None
        yield
        if self._created_id is not None:
            try:
                api_session.delete(f"{ADMIN_URL}/admin-api/risk/electronic-fence/delete", params={"id": self._created_id}, headers=auth_headers)
            except Exception as e:
                print(f"[cleanup] 删除失败 {self._created_id}: {e}")

    @pytest.mark.smoke
    def test_RiskElectronicFenceCreate(self, api_session, auth_headers, ok):
        url = f"{ADMIN_URL}/admin-api/risk/electronic-fence/create"
        body = {
              #"bizType": 0,
              "fenceName": "autotest",
              #"parentId": 17375,
              "fenceLevel": 1,
              #"shapeType": 1,
              #"geoJson": "",
              #"radius": 0,
              "status": 1,
              #"ruleId": 32049,
              "sortNum": 0,
              #"remark": "你说的对",
              "recyclePrice": 5537,
              #"clearPrice": 24336,
              #"provinceName": "张三",
              #"provinceCode": "",
              #"cityName": "张三",
              #"cityCode": "",
              #"districtName": "赵六",
              #"districtCode": "",
              "areaId": 2071771759382491137
            }
        r = ok(api_session.post(url, json=body, headers=auth_headers))
        self._created_id = r["data"] if isinstance(r["data"], (int, str)) and not isinstance(r["data"], bool) else (r["data"].get("id") if isinstance(r["data"], dict) else None)
