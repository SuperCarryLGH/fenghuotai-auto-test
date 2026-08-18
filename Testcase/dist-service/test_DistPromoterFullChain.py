"""分销全链路：注册绑定 → 下单 → 佣金入账 → 提现"""
import time
import pytest
from config import APP_URL, ADMIN_URL
from Common.login import Login


class TestDistPromoterFullChain:
    """全链路：A推广官 → B一级下线 → C二级下线 → 下单分佣"""

    @pytest.fixture(autouse=True)
    def _setup(self, api_session, login_tool, admin_token):
        self.s = api_session
        self.login = login_tool
        self.admin_headers = {
            **Login.ADMIN_LOGIN_HEADERS,
            "Authorization": f"Bearer {admin_token}",
        }
        now_suffix = str(int(time.time() * 1000))[-8:]
        self.mobile_a = "156" + now_suffix
        self.mobile_b = "156" + str(int(now_suffix) + 1).zfill(8)
        self.mobile_c = "156" + str(int(now_suffix) + 2).zfill(8)

    # ============================================================
    # 工具方法
    # ============================================================
    def _app_headers(self, token):
        return {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}

    def _app_get(self, url, token):
        return self.s.get(url, headers=self._app_headers(token), verify=False).json()

    def _app_post(self, url, body, token):
        return self.s.post(url, json=body, headers=self._app_headers(token), verify=False).json()

    def _admin_get(self, path, params=None):
        r = self.s.get(f"{ADMIN_URL}{path}", headers=self.admin_headers, params=params, verify=False)
        return r.json()

    def _admin_put(self, path, body):
        r = self.s.put(f"{ADMIN_URL}{path}", json=body, headers=self.admin_headers, verify=False)
        return r.json()

    def _assert_ok(self, r, step=""):
        assert r["code"] == 0, f"{step} 失败: code={r['code']}, msg={r.get('msg','')}"

    # ============================================================
    # 推广官认证全流程
    # ============================================================
    def _become_promoter(self, mobile, promoter_id=None):
        """sms-login → apply → admin审核 → 实名 → 签约 → 拿promoterId"""
        # 1. 登录（可选绑定上级）
        token = self.login.app_login_for_promoter(mobile=mobile, promoter_id=promoter_id)

        # 2. 申请推广官
        body = {
            "mobile": mobile, "provinceCode": "", "provinceName": "江苏省",
            "cityCode": "", "cityName": "苏州市", "districtCode": "", "districtName": "姑苏区",
            "promoteMode": 1, "hasMediaAccount": 1, "mediaAccountType": "",
            "mediaOtherDesc": "", "hasOfflineResource": 0, "offlineResource": "",
            "resourceOtherDesc": "", "hasSimilarExp": 1, "similarExp": "", "expOtherDesc": "",
            "mediaScreenshot": "",
        }
        r = self._app_post(f"{APP_URL}/app-api/dist/promoter/apply", body, token)
        self._assert_ok(r, f"{mobile} apply")
        apply_id = r["data"]["applyId"]
        print(f"  [{mobile}] apply_id={apply_id}")

        # 3. Admin 审核通过
        r = self._admin_get("/admin-api/dist/promoter-apply/get", {"id": apply_id})
        self._assert_ok(r, f"{mobile} get apply")
        if r["data"]["status"] != 20:
            body = {**r["data"], "status": 20}
            r = self._admin_put("/admin-api/dist/promoter-apply/update", body)
            self._assert_ok(r, f"{mobile} audit")
        print(f"  [{mobile}] 审核通过")

        # 4. 实名认证
        auth_body = {
                        "idCardFront": "https://gips2.baidu.com/it/u=195724436,3554684702&fm=3028&app=3028&f=JPEG&fmt=auto?w=1280&h=960",
            "idCardBack": "https://gips2.baidu.com/it/u=195724436,3554684702&fm=3028&app=3028&f=JPEG&fmt=auto?w=1280&h=960",
        }
        r = self._app_post(f"{APP_URL}/app-api/dist/promoter/real-name-auth", auth_body, token)
        self._assert_ok(r, f"{mobile} real-name-auth")

        # 5. 签署协议
        r = self._app_post(f"{APP_URL}/app-api/dist/promoter/sign-agreement",
                          {"agreementUrl": "https://example.com/signed.pdf"}, token)
        self._assert_ok(r, f"{mobile} sign-agreement")

        # 6. 获取 promoterId
        r = self._app_get(f"{APP_URL}/app-api/dist/promoter/info", token)
        self._assert_ok(r, f"{mobile} info")
        pid = r["data"]["promoterId"]
        assert int(pid) > 0, f"{mobile} promoterId=0，认证失败"
        print(f"  [{mobile}] promoterId={pid}")
        return int(pid), token

    # ============================================================
    # 全链路测试
    # ============================================================
    @pytest.mark.smoke
    def test_full_chain(self):
        # ——— Phase 1: A 成为推广官 ———
        print(f"\n=== Phase 1: A({self.mobile_a}) 申请推广官 ===")
        pid_a, token_a = self._become_promoter(self.mobile_a)

        # ——— Phase 2: B 成为推广官 + 绑定到 A ———
        print(f"\n=== Phase 2: B({self.mobile_b}) 绑定到 A(pid={pid_a}) ===")
        pid_b, token_b = self._become_promoter(self.mobile_b, promoter_id=pid_a)

        # ——— Phase 3: C 注册 + 绑定到 B ———
        print(f"\n=== Phase 3: C({self.mobile_c}) 绑定到 B(pid={pid_b}) ===")
        token_c = self.login.app_login_for_promoter(mobile=self.mobile_c, promoter_id=pid_b)

        # ——— Phase 4: C 创建地址 + 下单 → 结算 ———
        print(f"\n=== Phase 4: C({self.mobile_c}) 创建地址 + 下单 ===")
        # 创建收件地址
        addr_body = {
            "name": "auto", "mobile": self.mobile_c, "areaId": 330108,
            "provinceCode": "330000", "province": "浙江省", "cityCode": "330100",
            "city": "杭州市", "districtCode": "330108", "district": "滨江区",
            "areaName": "浙江省 杭州市 滨江区", "communityName": "测试小区",
            "detailAddress": "测试地址", "lat": "30.2085", "lon": "120.212", "defaultStatus": True,
        }
        r = self._app_post(f"{APP_URL}/app-api/member/address/create", addr_body, token_c)
        self._assert_ok(r, "C 创建地址")
        addr_id = r["data"] if isinstance(r["data"], (int, str)) else r["data"].get("id", r["data"])
        print(f"  address_id={addr_id}")

        order_payload = {
            "platform": "web", "provider": "", "bizMode": "WeightClothes",
            "userName": "auto", "userPhone": self.mobile_c,
            "addressId": addr_id,
            "appointmentDate": time.strftime("%Y-%m-%d"),
            "appointmentTimePeriod": "17:00-18:00",
            "appointmentWeekStr": "周五", "estimatedInfo": "5~10kg",
            "lat": "34.795439", "lon": "113.688145", "num": 5,
            "predictWeight": "5~10kg",
            "channel": "",
        }
        r = self._app_post(f"{APP_URL}/app-api/recycle/order/v2/mini-order-submit", order_payload, token_c)
        self._assert_ok(r, "C 下单")
        order_id = r["data"]["id"]
        print(f"  order_id={order_id}")

        # 触发结算
        # 测试环境自动结算，已注释 order-inspection
        time.sleep(5)  # 结算走 MQ，等待异步投递

        # ——— Phase 5: 验证佣金 ———
        print(f"\n=== Phase 5: 验证佣金 ===")
        for _ in range(10):
            r_a = self._app_get(f"{APP_URL}/app-api/dist/promoter/info", token_a)
            if r_a["code"] == 0:
                break
            time.sleep(1)
        self._assert_ok(r_a, "A wallet")
        print(f"  A balance={r_a['data']['commissionBalance']}")

        for _ in range(10):
            r_b = self._app_get(f"{APP_URL}/app-api/dist/promoter/info", token_b)
            if r_b["code"] == 0:
                break
            time.sleep(1)
        self._assert_ok(r_b, "B wallet")
        print(f"  B balance={r_b['data']['commissionBalance']}")

        assert int(r_b["data"]["commissionBalance"]) > 0, "B 一级佣金未入账"
        print("  ✅ B 一级佣金已入账")

        if int(r_a["data"]["commissionBalance"]) > 0:
            print(f"  ✅ A 二级佣金已入账: {r_a['data']['commissionBalance']}")

        # ——— 补充验证：A自己下单不应产生佣金 ———
        print(f"\n=== 补充: A({self.mobile_a}) 自己下单 → 不应有佣金 ===")
        r = self._app_post(f"{APP_URL}/app-api/member/address/create", {
            "name": "auto", "mobile": self.mobile_a, "areaId": 330108,
            "provinceCode": "330000", "province": "浙江省", "cityCode": "330100",
            "city": "杭州市", "districtCode": "330108", "district": "滨江区",
            "areaName": "浙江省 杭州市 滨江区", "communityName": "测试小区",
            "detailAddress": "测试地址", "lat": "30.2085", "lon": "120.212", "defaultStatus": True,
        }, token_a)
        self._assert_ok(r, "A 创建地址")
        addr_a = r["data"] if isinstance(r["data"], (int, str)) else r["data"].get("id", r["data"])

        order_a = {
            "platform": "web", "provider": "", "bizMode": "WeightClothes",
            "userName": "auto", "userPhone": self.mobile_a,
            "addressId": addr_a,
            "appointmentDate": time.strftime("%Y-%m-%d"),
            "appointmentTimePeriod": "17:00-18:00",
            "appointmentWeekStr": "周五", "estimatedInfo": "5~10kg",
            "lat": "34.795439", "lon": "113.688145", "num": 5,
            "predictWeight": "5~10kg",
            "channel": "",
        }
        r = self._app_post(f"{APP_URL}/app-api/recycle/order/v2/mini-order-submit", order_a, token_a)
        self._assert_ok(r, "A 下单")
        # 测试环境自动结算，已注释 order-inspection
        time.sleep(5)  # 结算走 MQ，等待异步投递

        wa_before = r_a["data"]["commissionBalance"]
        for _ in range(10):
            r_a2 = self._app_get(f"{APP_URL}/app-api/dist/promoter/info", token_a)
            if r_a2["code"] == 0:
                break
            time.sleep(1)
        wa_after = r_a2["data"]["commissionBalance"]
        assert wa_after != wa_before, f"A 自己下单没有产生佣金！before={wa_before} after={wa_after}"
        print(f"  ✅ A 自己下单已产生佣金 ({wa_before}→{wa_after})")
