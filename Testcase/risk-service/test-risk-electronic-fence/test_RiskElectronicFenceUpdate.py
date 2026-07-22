import pytest
from config import ADMIN_URL


class TestRiskElectronicFenceUpdate:
    """更新风控-电子围栏主"""

    @pytest.mark.smoke
    def test_RiskElectronicFenceUpdate(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/risk/electronic-fence/update"
        body = {
              "id": 9999999998,
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
              "areaId": 2071771759382491138
        }
        resp = api_session.put(url, json=body, headers=auth_headers)
        assert resp.status_code == 200
