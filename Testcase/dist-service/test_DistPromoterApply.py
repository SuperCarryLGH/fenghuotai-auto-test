"""推广达人申请"""
import time

import pytest
from config import APP_URL


class TestDistPromoterApply:
    """申请推广达人：全新手机号可申请成功；重复申请会被拒绝"""
    URL = f"{APP_URL}/app-api/dist/promoter/apply"

    def _new_mobile(self):
        return "156" + str(int(time.time() * 1000))[-8:]

    def _apply_body(self, mobile):
        return {
            "mobile": mobile, "provinceCode": "", "provinceName": "江苏省",
            "cityCode": "", "cityName": "苏州市", "districtCode": "", "districtName": "姑苏区",
            "promoteMode": 1, "hasMediaAccount": 1, "mediaAccountType": "",
            "mediaOtherDesc": "", "hasOfflineResource": 0, "offlineResource": "",
            "resourceOtherDesc": "", "hasSimilarExp": 1, "similarExp": "", "expOtherDesc": "",
            "mediaScreenshot": "",
        }

    @pytest.mark.smoke
    def test_DistPromoterApply(self, api_session, login_tool):
        mobile = self._new_mobile()
        token = login_tool.app_login(mobile=mobile)
        headers = {"Authorization": f"Bearer {token}"}

        # 1. 首次申请 → 成功（返回 applyId）
        r1 = api_session.post(self.URL, json=self._apply_body(mobile), headers=headers)
        assert r1.status_code == 200
        data1 = r1.json()
        assert data1["code"] == 0 or data1["code"] == "0", \
            f"首次申请推广达人失败: {data1}"
        print(f"  首次申请成功: {data1}")

        # 2. 重复申请 → 拒绝（已申请/已开通）
        r2 = api_session.post(self.URL, json=self._apply_body(mobile), headers=headers)
        assert r2.status_code == 200
        data2 = r2.json()
        assert data2["code"] != 0 and data2["code"] != "0", \
            f"重复申请应被拒绝，实际成功: {data2}"
        print(f"  重复申请被拒（符合预期）: {data2}")
