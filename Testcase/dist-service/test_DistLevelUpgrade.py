"""等级升级：达单量阈值后自动升级"""
import time
import pytest
from config import APP_URL, ADMIN_URL
from Common.login import Login

ID_CARD = "https://gips2.baidu.com/it/u=195724436,3554684702&fm=3028&app=3028&f=JPEG&fmt=auto?w=1280&h=960"


class TestDistLevelUpgrade:
    """推广官等级达标自动升级"""

    @pytest.fixture(autouse=True)
    def _setup(self, api_session, login_tool, admin_token, db_client):
        self.s = api_session
        self.login = login_tool
        self.db = db_client
        self.admin_headers = {
            **Login.ADMIN_LOGIN_HEADERS,
            "Authorization": f"Bearer {admin_token}",
        }
        self.mobile_a = "156" + str(int(time.time() * 1000))[-8:]

    def _app_headers(self, token):
        return {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}

    def _assert_ok(self, r, step=""):
        assert r["code"] == 0, f"{step} 失败: code={r['code']}, msg={r.get('msg','')}"

    def _wait_db(self, sql, params, predicate, timeout=10):
        for _ in range(timeout * 2):
            row = self.db.fetch_one(sql, params)
            if row and predicate(row):
                return row
            time.sleep(0.5)
        return self.db.fetch_one(sql, params)

    def _become_promoter(self, mobile, promoter_id=None):
        token = self.login.app_login_for_promoter(mobile=mobile, promoter_id=promoter_id)
        body = {"mobile": mobile, "provinceCode": "", "provinceName": "江苏省",
                "cityCode": "", "cityName": "苏州市", "districtCode": "", "districtName": "姑苏区",
                "promoteMode": 1, "hasMediaAccount": 1, "mediaAccountType": "",
                "mediaOtherDesc": "", "hasOfflineResource": 0, "offlineResource": "",
                "resourceOtherDesc": "", "hasSimilarExp": 1, "similarExp": "", "expOtherDesc": "",
                "mediaScreenshot": ""}
        r = self.s.post(f"{APP_URL}/app-api/dist/promoter/apply", json=body,
                        headers=self._app_headers(token), verify=False).json()
        self._assert_ok(r, f"{mobile} apply")
        apply_id = r["data"]["applyId"]
        r = self.s.get(f"{ADMIN_URL}/admin-api/dist/promoter-apply/get",
                       headers=self.admin_headers, params={"id": apply_id}, verify=False).json()
        self._assert_ok(r, f"{mobile} get apply")
        if r["data"]["status"] != 20:
            body = {**r["data"], "status": 20}
            self._assert_ok(self.s.put(f"{ADMIN_URL}/admin-api/dist/promoter-apply/update",
                            json=body, headers=self.admin_headers, verify=False).json(), f"{mobile} audit")
        self._assert_ok(self.s.post(f"{APP_URL}/app-api/dist/promoter/real-name-auth",
                        json={"idCardFront": ID_CARD, "idCardBack": ID_CARD},
                        headers=self._app_headers(token), verify=False).json(), "real-name")
        self._assert_ok(self.s.post(f"{APP_URL}/app-api/dist/promoter/sign-agreement",
                        json={"agreementUrl": "https://e.com/s.pdf"},
                        headers=self._app_headers(token), verify=False).json(), "sign")
        r = self.s.get(f"{APP_URL}/app-api/dist/promoter/info",
                       headers=self._app_headers(token), verify=False).json()
        self._assert_ok(r, "info")
        assert int(r["data"]["promoterId"]) > 0
        return r["data"]["promoterId"], token

    def _settle_order(self, token, mobile):
        r = self.s.post(f"{APP_URL}/app-api/member/address/create", json={
            "name": "auto", "mobile": mobile, "areaId": 330108,
            "provinceCode": "330000", "province": "浙江省", "cityCode": "330100",
            "city": "杭州市", "districtCode": "330108", "district": "滨江区",
            "areaName": "浙江省 杭州市 滨江区", "communityName": "测试小区",
            "detailAddress": "测试地址", "lat": "30.2085", "lon": "120.212", "defaultStatus": True,
        }, headers=self._app_headers(token), verify=False).json()
        self._assert_ok(r, f"{mobile} 地址")
        addr_id = r["data"] if isinstance(r["data"], (int, str)) else r["data"].get("id", r["data"])
        r = self.s.post(f"{APP_URL}/app-api/recycle/order/v2/mini-order-submit", json={
            "platform": "web", "provider": "", "bizMode": "WeightClothes",
            "userName": "auto", "userPhone": mobile,
            "addressId": addr_id,
            "appointmentDate": time.strftime("%Y-%m-%d"),
            "appointmentTimePeriod": "17:00-18:00", "appointmentWeekStr": "周五",
            "estimatedInfo": "5~10kg", "lat": "34.795439", "lon": "113.688145",
            "num": 5, "predictWeight": "5~10kg",
            "channel": "",
        }, headers=self._app_headers(token), verify=False).json()
        self._assert_ok(r, f"{mobile} 下单")
        order_id = r["data"]["id"]
        # 测试环境自动结算，已注释 order-inspection
        time.sleep(2)
        return order_id

    def _level(self, mobile):
        r = self.s.get(f"{APP_URL}/app-api/dist/promoter/info",
                       headers=self._app_headers(
                           self.login.app_login_for_promoter(mobile=mobile)),
                       verify=False).json()
        self._assert_ok(r, f"{mobile} info")
        return r["data"]["level"]

    def _upgrade_order_target(self, token):
        r = self.s.get(f"{APP_URL}/app-api/dist/rule/get",
                       params={"promoteType": 10},
                       headers=self._app_headers(token), verify=False).json()
        self._assert_ok(r, "load rules")
        rules = r["data"]
        target = rules[0]["upgradeOrderTarget"] if rules else 20
        print(f"  升级阈值: {target} 单")
        return target

    def test_upgrade_on_order_threshold(self):
        print("\n=== 等级升级 ===")
        pid_a, token_a = self._become_promoter(self.mobile_a)
        target = self._upgrade_order_target(token_a)
        level_before = self._level(self.mobile_a)
        print(f"  初始等级: {level_before}")
        for i in range(target + 1):
            suffix = str(int(time.time() * 1000))[-8:]
            mobile_down = "156" + str(int(suffix) + i).zfill(8)
            self.login.app_login_for_promoter(mobile=mobile_down, promoter_id=pid_a)
            token = self.login.app_login_for_promoter(mobile=mobile_down)
            self._settle_order(token, mobile_down)
            print(f"  [{i+1}/{target}] {mobile_down} 下单完成")
        level_after = level_before
        for _ in range(60):
            level_after = self._level(self.mobile_a)
            if int(level_after) > int(level_before):
                break
            time.sleep(1)
        print(f"  升级后等级: {level_after}")
        assert int(level_after) > int(level_before), f"等级未升级: {level_before}→{level_after}"
        print(f"  ✅ 等级 {level_before} → {level_after}")
