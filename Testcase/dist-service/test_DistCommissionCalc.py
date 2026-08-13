"""佣金计算：DB 查询 real_weight/total_price → 匹配规则 → 校验 dist_commission_record"""
import time
import pytest
from config import APP_URL, ADMIN_URL
from Common.login import Login

ID_CARD = "https://gips2.baidu.com/it/u=195724436,3554684702&fm=3028&app=3028&f=JPEG&fmt=auto?w=1280&h=960"


class TestDistCommissionCalc:
    """订单结算后 DB 校验佣金金额"""

    @pytest.fixture(autouse=True)
    def _setup(self, api_session, login_tool, admin_token, db_client):
        self.s = api_session
        self.login = login_tool
        self.db = db_client
        self.admin_headers = {
            **Login.ADMIN_LOGIN_HEADERS,
            "Authorization": f"Bearer {admin_token}",
        }
        now_suffix = str(int(time.time() * 1000))[-8:]
        self.mobile_a = "156" + now_suffix
        self.mobile_b = "156" + str(int(now_suffix) + 1).zfill(8)

    # ============================================================
    # 通用工具
    # ============================================================
    def _app_headers(self, token):
        return {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}

    def _assert_ok(self, r, step=""):
        assert r["code"] == 0, f"{step} 失败: code={r['code']}, msg={r.get('msg','')}"

    def _load_rules(self, token):
        r = self.s.get(f"{APP_URL}/app-api/dist/rule/get",
                       params={"promoteType": 10},
                       headers=self._app_headers(token), verify=False).json()
        self._assert_ok(r, "load rules")
        return r["data"]

    # ============================================================
    # 推广官认证
    # ============================================================
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
            r = self.s.put(f"{ADMIN_URL}/admin-api/dist/promoter-apply/update",
                           json=body, headers=self.admin_headers, verify=False).json()
            self._assert_ok(r, f"{mobile} audit")
        self._assert_ok(self.s.post(f"{APP_URL}/app-api/dist/promoter/real-name-auth",
                        json={"idCardFront": ID_CARD, "idCardBack": ID_CARD},
                        headers=self._app_headers(token), verify=False).json(), f"{mobile} real-name")
        self._assert_ok(self.s.post(f"{APP_URL}/app-api/dist/promoter/sign-agreement",
                        json={"agreementUrl": "https://e.com/s.pdf"},
                        headers=self._app_headers(token), verify=False).json(), f"{mobile} sign")
        r = self.s.get(f"{APP_URL}/app-api/dist/promoter/info",
                       headers=self._app_headers(token), verify=False).json()
        self._assert_ok(r, f"{mobile} info")
        pid = r["data"]["promoterId"]
        assert int(pid) > 0, f"{mobile} promoterId=0"
        return int(pid), token

    # ============================================================
    # 下单
    # ============================================================
    def _settle_order(self, token, mobile, num=5, predict_weight="5~10kg"):
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
            "estimatedInfo": predict_weight, "lat": "34.795439", "lon": "113.688145",
            "num": num, "predictWeight": predict_weight,
            "channel": "",
        }, headers=self._app_headers(token), verify=False).json()
        self._assert_ok(r, f"{mobile} 下单")
        order_id = r["data"]["id"]
        # 等 mock 完成订单 + 自动结算写入 DB
        time.sleep(2)
        return order_id

    # ============================================================
    # 新增辅助方法
    # ============================================================
    def _get_order_data(self, order_id):
        """查 recycle_order → (real_weight, total_price)"""
        row = self.db.fetch_one(
            "SELECT real_weight, total_price FROM recycle_order WHERE id=%s", (order_id,))
        assert row, f"order_id={order_id} 不存在"
        return float(row["real_weight"]), float(row["total_price"])

    def _get_promoter_info(self, token):
        """/promoter/info → {level, star}"""
        r = self.s.get(f"{APP_URL}/app-api/dist/promoter/info",
                       headers=self._app_headers(token), verify=False).json()
        self._assert_ok(r, "promoter info")
        data = r["data"]
        return {"level": data["level"], "star": data["star"]}

    def _match_rule_detail(self, rules, level, star, real_weight):
        """level+star 匹配规则 → weight 区间匹配 detail"""
        rule = None
        for r in rules:
            if r["level"] == level and r["star"] == star:
                rule = r
                break
        assert rule, f"未匹配到规则: level={level} star={star}"
        for d in rule["ruleDetails"]:
            if d["weightMin"] <= real_weight <= d["weightMax"]:
                return rule, d
        raise AssertionError(
            f"未匹配到 weight 区间: real_weight={real_weight}, details={rule['ruleDetails']}")

    def _calc_expected(self, detail, total_price):
        """rewardMode=1: 固定值; rewardMode=2: 比例"""
        if detail["rewardMode"] == 1:
            return detail["firstFixedReward"], detail["secondFixedReward"]
        else:
            return total_price * detail["firstOrderRate"], total_price * detail["secondOrderRate"]

    def _wait_commission(self, order_id, promoter_id, timeout=20):
        """轮询 dist_commission_record（status=1），返回 price 或 None"""
        time.sleep(5)  # 结算走 MQ，等待异步投递
        for _ in range(timeout * 2):
            row = self.db.fetch_one(
                "SELECT r.price FROM dist_commission_record r "
                "JOIN dist_commission_account a ON r.commission_account_id = a.id "
                "WHERE r.order_id=%s AND a.account_id=%s AND r.income_target_type=10 AND r.status=1",
                (order_id, promoter_id))
            if row:
                return float(row["price"])
            time.sleep(0.5)
        return None

    def _assert_commission(self, order_id, promoter_id, expected, label=""):
        """校验佣金入账，失败时打印详情"""
        actual = self._wait_commission(order_id, promoter_id)
        if actual is None:
            record = self.db.fetch_one(
                "SELECT r.*, a.account_id FROM dist_commission_record r "
                "JOIN dist_commission_account a ON r.commission_account_id = a.id "
                "WHERE r.order_id=%s AND a.account_id=%s",
                (order_id, promoter_id))
            print(f"  ❌ {label} 未找到已入账佣金记录")
            print(f"  完整记录: {record}")
            raise AssertionError(f"{label} 佣金未入账")
        if actual != expected:
            order = self.db.fetch_one(
                "SELECT real_weight, total_price FROM recycle_order WHERE id=%s", (order_id,))
            print(f"  ❌ {label} 佣金不匹配")
            print(f"  理应入账: {expected}")
            print(f"  实际入账: {actual}")
            print(f"  订单信息: weight={order['real_weight']}, price={order['total_price']}")
            raise AssertionError(f"{label}: 预期={expected}, 实际={actual}")
        print(f"  ✅ {label} 佣金={actual}")

    # ============================================================
    # 测试方法
    # ============================================================
    def test_basic_level1_commission(self):
        print(f"\n=== 基础一级佣金 ===")
        pid_a, token_a = self._become_promoter(self.mobile_a)
        mobile_c = "156" + str(int(time.time() * 1000))[-8:]
        token_c = self.login.app_login_for_promoter(mobile=mobile_c, promoter_id=pid_a)

        order_id = self._settle_order(token_c, mobile_c)
        real_weight, total_price = self._get_order_data(order_id)
        rules = self._load_rules(token_a)
        info = self._get_promoter_info(token_a)
        _, detail = self._match_rule_detail(rules, info["level"], info["star"], real_weight)
        expected, _ = self._calc_expected(detail, total_price)
        print(f"  weight={real_weight}, price={total_price}, 预期一级佣金={expected}")
        self._assert_commission(order_id, pid_a, expected, "A一级")

    def test_level2_commission(self):
        print(f"\n=== 二级佣金 ===")
        pid_a, token_a = self._become_promoter(self.mobile_a)
        pid_b, token_b = self._become_promoter(self.mobile_b, promoter_id=pid_a)
        mobile_c = "156" + str(int(time.time() * 1000))[-8:]
        token_c = self.login.app_login_for_promoter(mobile=mobile_c, promoter_id=pid_b)

        order_id = self._settle_order(token_c, mobile_c)
        real_weight, total_price = self._get_order_data(order_id)
        rules = self._load_rules(token_a)
        info = self._get_promoter_info(token_a)
        _, detail = self._match_rule_detail(rules, info["level"], info["star"], real_weight)
        expected_first, expected_second = self._calc_expected(detail, total_price)
        print(f"  weight={real_weight}, price={total_price}")
        print(f"  预期一级佣金={expected_first}, 二级佣金={expected_second}")
        self._assert_commission(order_id, pid_b, expected_first, "B一级")
        self._assert_commission(order_id, pid_a, expected_second, "A二级")

    def test_boundary_weight_levels(self):
        print(f"\n=== 边界测试: 不同重量区间的佣金 ===")
        pid_a, token_a = self._become_promoter(self.mobile_a)
        suffix = str(int(time.time() * 1000))[-8:]
        mobile_c1 = "156" + suffix
        mobile_c2 = "156" + str(int(suffix) + 1).zfill(8)
        token_c1 = self.login.app_login_for_promoter(mobile=mobile_c1, promoter_id=pid_a)
        token_c2 = self.login.app_login_for_promoter(mobile=mobile_c2, promoter_id=pid_a)

        order_id_1 = self._settle_order(token_c1, mobile_c1, num=1, predict_weight="0~5kg")
        order_id_2 = self._settle_order(token_c2, mobile_c2, num=50, predict_weight="21~50kg")

        rules = self._load_rules(token_a)
        info = self._get_promoter_info(token_a)

        for label, oid in [("小订单(≤20kg)", order_id_1), ("大订单(≥21kg)", order_id_2)]:
            real_weight, total_price = self._get_order_data(oid)
            _, detail = self._match_rule_detail(rules, info["level"], info["star"], real_weight)
            expected, _ = self._calc_expected(detail, total_price)
            print(f"  {label}: weight={real_weight}, price={total_price}, 预期佣金={expected}")
            self._assert_commission(oid, pid_a, expected, label)

    def test_self_order_no_commission(self):
        print(f"\n=== 推广官自己下单无佣金 ===")
        pid_a, token_a = self._become_promoter(self.mobile_a)
        order_id = self._settle_order(token_a, self.mobile_a)
        for i in range(10):
            row = self.db.fetch_one(
                "SELECT COUNT(*) as cnt FROM dist_commission_record r "
                "JOIN dist_commission_account a ON r.commission_account_id = a.id "
                "WHERE r.order_id=%s AND a.account_id=%s AND r.income_target_type=10",
                (order_id, pid_a))
            if row["cnt"] == 0:
                break
            time.sleep(0.5)
        else:
            row = self.db.fetch_one(
                "SELECT r.price FROM dist_commission_record r "
                "JOIN dist_commission_account a ON r.commission_account_id = a.id "
                "WHERE r.order_id=%s AND a.account_id=%s AND r.income_target_type=10",
                (order_id, pid_a))
            raise AssertionError(f"推广官自己下单产生了佣金: {row}")
        print(f"  ✅ 推广官自己下单未产生佣金")
