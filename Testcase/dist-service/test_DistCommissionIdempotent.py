"""佣金幂等：同一订单重复结算不重复发佣（测试环境自动结算，暂跳过）"""
import time
import pytest
from config import APP_URL, ADMIN_URL
from Common.login import Login

ID_CARD = "https://gips2.baidu.com/it/u=195724436,3554684702&fm=3028&app=3028&f=JPEG&fmt=auto?w=1280&h=960"


class TestDistCommissionIdempotent:
    """order-inspection 重复调用 → 佣金不重复发放"""

    @pytest.fixture(autouse=True)
    def _setup(self, api_session, login_tool, admin_token, db_client):
        self.s = api_session
        self.login = login_tool
        self.db = db_client
        self.admin_headers = {
            **Login.ADMIN_LOGIN_HEADERS,
            "Authorization": f"Bearer {admin_token}",
        }
        now = str(int(time.time() * 1000))[-8:]
        self.mobile_a = "159" + now
        self.mobile_b = "159" + str(int(now) + 1)

    def _app_headers(self, token):
        return {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}

    def _assert_ok(self, r, step=""):
        assert r["code"] == 0, f"{step}: code={r['code']} msg={r.get('msg','')}"

    def _wait_db(self, sql, params, predicate, timeout=10):
        for _ in range(timeout * 2):
            row = self.db.fetch_one(sql, params)
            if row and predicate(row):
                return row
            time.sleep(0.5)
        return self.db.fetch_one(sql, params)

    @pytest.mark.skip(reason="测试环境自动结算，暂无手动触发方式")
    def test_duplicate_settle_no_duplicate_commission(self):
        print("\n=== 幂等: 重复结算 → 佣金不重复 ===")
        pid_a, _ = self._become_promoter(self.mobile_a)
        _, token_b = self._become_promoter(self.mobile_b, promoter_id=pid_a)
        r = self.s.post(f"{APP_URL}/app-api/member/address/create", json={
            "name": "auto", "mobile": self.mobile_b, "areaId": 330108,
            "provinceCode": "330000", "province": "浙江省", "cityCode": "330100",
            "city": "杭州市", "districtCode": "330108", "district": "滨江区",
            "areaName": "浙江省 杭州市 滨江区", "communityName": "测试小区",
            "detailAddress": "测试地址", "lat": "30.2085", "lon": "120.212", "defaultStatus": True,
        }, headers=self._app_headers(token_b), verify=False).json()
        self._assert_ok(r, "地址")
        addr_id = r["data"] if isinstance(r["data"], (int, str)) else r["data"].get("id", r["data"])
        r = self.s.post(f"{APP_URL}/app-api/recycle/order/v2/mini-order-submit", json={
            "platform": "web", "provider": "", "bizMode": "WeightClothes",
            "userName": "auto", "userPhone": self.mobile_b,
            "addressId": addr_id,
            "appointmentDate": time.strftime("%Y-%m-%d"),
            "appointmentTimePeriod": "17:00-18:00", "appointmentWeekStr": "周五",
            "estimatedInfo": "5~10kg", "lat": "34.795439", "lon": "113.688145",
            "num": 5, "predictWeight": "5~10kg",
            "channel": "",
        }, headers=self._app_headers(token_b), verify=False).json()
        self._assert_ok(r, "下单")
        order_id = r["data"]["id"]
        r = self.s.put(f"{ADMIN_URL}/admin-api/recycle/admin-order/order-inspection",
                       json={"orderId": order_id}, headers=self.admin_headers, verify=False)
         # settle (empty body)
        assert r.status_code == 200, "第一次结算"
        time.sleep(3)
        row = self._wait_db(
            "SELECT COUNT(*) as cnt FROM dist_commission_record WHERE order_id=%s", (order_id,),
            lambda r: True)
        first_cnt = row["cnt"] if row else 0
        print(f"  第一次结算后佣金记录: {first_cnt} 条")
        r = self.s.put(f"{ADMIN_URL}/admin-api/recycle/admin-order/order-inspection",
                       json={"orderId": order_id}, headers=self.admin_headers, verify=False)
        time.sleep(2)
        row = self._wait_db(
            "SELECT COUNT(*) as cnt FROM dist_commission_record WHERE order_id=%s", (order_id,),
            lambda r: True)
        second_cnt = row["cnt"] if row else 0
        print(f"  第二次结算后佣金记录: {second_cnt} 条")
        assert second_cnt == first_cnt, \
            f"幂等失败! 重复结算导致佣金记录从{first_cnt}变成{second_cnt}"
        print(f"  ✅ 幂等校验通过 ({first_cnt}→{second_cnt})")

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
                            json=body, headers=self.admin_headers, verify=False).json(), "audit")
        self._assert_ok(self.s.post(f"{APP_URL}/app-api/dist/promoter/real-name-auth",
                        json={"idCardFront": ID_CARD, "idCardBack": ID_CARD},
                        headers=self._app_headers(token), verify=False).json(), "real-name")
        self._assert_ok(self.s.post(f"{APP_URL}/app-api/dist/promoter/sign-agreement",
                        json={"agreementUrl": "https://e.com/s.pdf"},
                        headers=self._app_headers(token), verify=False).json(), "sign")
        r = self.s.get(f"{APP_URL}/app-api/dist/promoter/info",
                       headers=self._app_headers(token), verify=False).json()
        self._assert_ok(r, "info")
        return r["data"]["promoterId"], token
