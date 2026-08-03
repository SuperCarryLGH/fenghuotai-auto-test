"""团队测试公用工具"""
import random
import time
from config import APP_URL, ADMIN_URL
from Common.login import Login

ID_CARD = "https://gips2.baidu.com/it/u=195724436,3554684702&fm=3028&app=3028&f=JPEG&fmt=auto?w=1280&h=960"


class TeamUtils:
    """封装团队测试通用操作"""

    def __init__(self, api_session, login_tool, db_client, admin_token):
        self.s = api_session
        self.login = login_tool
        self.db = db_client
        self.admin_headers = {
            **Login.ADMIN_LOGIN_HEADERS,
            "Authorization": f"Bearer {admin_token}",
        }

    # ============================================================
    # 底层工具
    # ============================================================
    # 进程内自增序号 + 已用集合，避免同毫秒撞号（旧实现 2 万次调用仅 18 个唯一）
    _seq = random.randint(0, 99)
    _used_mobiles = set()

    @staticmethod
    def gen_mobile():
        while True:
            TeamUtils._seq += 1
            seq = TeamUtils._seq % 100
            num = "156" + str(int(time.time() * 1000))[-6:] + str(seq).zfill(2)
            if num not in TeamUtils._used_mobiles:
                TeamUtils._used_mobiles.add(num)
                return num

    def app_headers(self, token):
        return {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}

    def assert_ok(self, r, step=""):
        assert r["code"] == 0, f"{step}: code={r['code']}, msg={r.get('msg','')}"

    # ============================================================
    # 推广官认证（同个人佣金测试）
    # ============================================================
    def become_promoter(self, mobile, promoter_id=None):
        token = self.login.app_login_for_promoter(mobile=mobile, promoter_id=promoter_id)
        body = {"mobile": mobile, "provinceCode": "", "provinceName": "江苏省",
                "cityCode": "", "cityName": "苏州市", "districtCode": "", "districtName": "姑苏区",
                "promoteMode": 1, "hasMediaAccount": 1, "mediaAccountType": "",
                "mediaOtherDesc": "", "hasOfflineResource": 0, "offlineResource": "",
                "resourceOtherDesc": "", "hasSimilarExp": 1, "similarExp": "", "expOtherDesc": "",
                "mediaScreenshot": ""}
        r = self.s.post(f"{APP_URL}/app-api/dist/promoter/apply", json=body,
                        headers=self.app_headers(token), verify=False).json()
        if r["code"] == 0:
            apply_id = r["data"]["applyId"]
            r = self.s.get(f"{ADMIN_URL}/admin-api/dist/promoter-apply/get",
                           headers=self.admin_headers, params={"id": apply_id}, verify=False).json()
            self.assert_ok(r, f"{mobile} get apply")
            if r["data"]["status"] != 20:
                body = {**r["data"], "status": 20}
                self.assert_ok(self.s.put(f"{ADMIN_URL}/admin-api/dist/promoter-apply/update",
                               json=body, headers=self.admin_headers, verify=False).json(),
                               f"{mobile} audit")
        r = self.s.post(f"{APP_URL}/app-api/dist/promoter/real-name-auth",
                        json={"idCardFront": ID_CARD, "idCardBack": ID_CARD},
                        headers=self.app_headers(token), verify=False).json()
        if r["code"] == 10024:
            pass
        else:
            self.assert_ok(r, f"{mobile} real-name")
        r = self.s.post(f"{APP_URL}/app-api/dist/promoter/sign-agreement",
                        json={"agreementUrl": "https://e.com/s.pdf"},
                        headers=self.app_headers(token), verify=False).json()
        if r["code"] == 10023:
            pass
        else:
            self.assert_ok(r, f"{mobile} sign")
        r = self.s.get(f"{APP_URL}/app-api/dist/promoter/info",
                       headers=self.app_headers(token), verify=False).json()
        self.assert_ok(r, f"{mobile} info")
        pid = r["data"]["promoterId"]
        assert int(pid) > 0, f"{mobile} promoterId=0"
        return int(pid), token

    # ============================================================
    # 团队创建
    # ============================================================
    def become_team_leader(self, mobile, team_type=1, team_name=None):
        pid, token = self.become_promoter(mobile)
        if not team_name:
            team_name = f"team_{mobile[-4:]}"
        r = self.s.post(f"{APP_URL}/app-api/dist/team/apply", json={
            "teamType": team_type, "teamName": team_name,
            "mobile": mobile, "address": "测试地址",
            "socialAccount": "微信", "groupChannel": "微信社群",
        }, headers=self.app_headers(token), verify=False).json()
        self.assert_ok(r, f"{mobile} team apply")
        apply_id = r["data"]["applyId"]
        r = self.s.get(f"{ADMIN_URL}/admin-api/dist/team-apply/get",
                       headers=self.admin_headers, params={"id": apply_id}, verify=False).json()
        self.assert_ok(r, f"{mobile} get team apply")
        self.assert_ok(self.s.post(f"{ADMIN_URL}/admin-api/dist/team/apply-audit",
                        json={"id": apply_id, "status": 20},
                        headers=self.admin_headers, verify=False).json(), f"{mobile} audit team")
        r = self.s.get(f"{APP_URL}/app-api/dist/promoter/info",
                       headers=self.app_headers(token), verify=False).json()
        self.assert_ok(r, f"{mobile} info after team")
        team_info = r["data"]["teamInfo"]
        team_id = int(team_info["teamId"])
        assert team_id > 0, f"{mobile} teamId=0"
        return team_id, pid, token, team_info

    # ============================================================
    # 入团
    # ============================================================
    def join_team(self, mobile, team_id):
        """入团：团队 join 要求加入者已是推广员，非推广员先补注册"""
        if self.db is not None:
            row = self.db.fetch_one(
                "SELECT p.id FROM dist_promoter p "
                "JOIN member_user u ON p.user_id = u.id "
                "WHERE u.mobile=%s AND p.deleted=0 AND u.deleted=0",
                (mobile,))
            if row:
                token = self.login.app_login_for_promoter(mobile=mobile)
            else:
                _, token = self.become_promoter(mobile)
        else:
            token = self.login.app_login_for_promoter(mobile=mobile)
        r = self.s.post(f"{APP_URL}/app-api/dist/team/join", json={"teamId": team_id},
                        headers=self.app_headers(token), verify=False).json()
        self.assert_ok(r, f"{mobile} join team")
        apply_id = r["data"]["applyId"]
        return token, apply_id

    def audit_join(self, apply_id, leader_token, status=20, remark=None):
        body = {"applyId": apply_id, "status": status}
        if remark:
            body["auditRemark"] = remark
        self.assert_ok(self.s.post(f"{APP_URL}/app-api/dist/team/join-audit",
                        json=body,
                        headers=self.app_headers(leader_token), verify=False).json(),
                       f"audit join {apply_id}")

    # ============================================================
    # 下单
    # ============================================================
    def settle_order(self, token, mobile, num=5, predict_weight="5~10kg"):
        r = self.s.post(f"{APP_URL}/app-api/member/address/create", json={
            "name": "auto", "mobile": mobile, "areaId": 330108,
            "provinceCode": "330000", "province": "浙江省", "cityCode": "330100",
            "city": "杭州市", "districtCode": "330108", "district": "滨江区",
            "areaName": "浙江省 杭州市 滨江区", "communityName": "测试小区",
            "detailAddress": "测试地址", "lat": "30.2085", "lon": "120.212", "defaultStatus": True,
        }, headers=self.app_headers(token), verify=False).json()
        self.assert_ok(r, f"{mobile} 地址")
        addr_id = r["data"] if isinstance(r["data"], (int, str)) else r["data"].get("id", r["data"])
        r = self.s.post(f"{APP_URL}/app-api/recycle/order/v2/mini-order-submit", json={
            "platform": "web", "provider": "", "bizMode": "WeightClothes",
            "userName": "auto", "userPhone": mobile,
            "addressId": addr_id,
            "appointmentDate": time.strftime("%Y-%m-%d"),
            "appointmentTimePeriod": "17:00-18:00", "appointmentWeekStr": "周五",
            "estimatedInfo": predict_weight, "lat": "34.795439", "lon": "113.688145",
            "num": num, "predictWeight": predict_weight, "channel": "",
        }, headers=self.app_headers(token), verify=False).json()
        self.assert_ok(r, f"{mobile} 下单")
        order_id = r["data"]["id"]
        time.sleep(2)
        return order_id

    # ============================================================
    # 规则匹配
    # ============================================================
    def load_team_rules(self, token):
        r = self.s.get(f"{APP_URL}/app-api/dist/rule/get", params={"promoteType": 20},
                       headers=self.app_headers(token), verify=False).json()
        self.assert_ok(r, "load team rules")
        return r["data"]

    def load_personal_rules(self, token):
        r = self.s.get(f"{APP_URL}/app-api/dist/rule/get", params={"promoteType": 10},
                       headers=self.app_headers(token), verify=False).json()
        self.assert_ok(r, "load personal rules")
        return r["data"]

    def match_rule_detail(self, rules, level, star, real_weight):
        rule = None
        for r in rules:
            if r["level"] == level and r["star"] == star:
                rule = r
                break
        assert rule, f"未匹配到规则: level={level} star={star}"
        for d in rule["ruleDetails"]:
            if d["weightMin"] <= real_weight <= d["weightMax"]:
                return rule, d
        raise AssertionError(f"未匹配到 weight 区间: real_weight={real_weight}, details={rule['ruleDetails']}")

    def calc_team_split(self, detail, total_price):
        """
        按个人逻辑计算佣金 base，团长佣金按团队分成比例拆分。
        分成比例未配置(None)时全部分给团队（当前 dev 行为）。
        返回: (一级个人, 二级个人, 团队)
        """
        rm = detail["rewardMode"]
        l1 = detail["firstFixedReward"] if rm == 1 else total_price * detail["firstOrderRate"]
        l2 = detail["secondFixedReward"] if rm == 1 else total_price * detail["secondOrderRate"]
        rate = detail["secondOrderTeamRewardRate"]
        team = int(l2 * (rate if rate is not None else 1.0))
        return l1, l2 - team, team

    # ============================================================
    # DB 查询
    # ============================================================
    def get_promoter_id_by_mobile(self, mobile):
        """通过手机号查推广员ID"""
        row = self.db.fetch_one(
            "SELECT p.id FROM dist_promoter p "
            "JOIN member_user u ON p.user_id = u.id "
            "WHERE u.mobile=%s AND p.deleted=0 AND u.deleted=0",
            (mobile,))
        assert row, f"mobile={mobile} 未找到推广员"
        return int(row["id"])

    def get_order_data(self, order_id):
        row = self.db.fetch_one(
            "SELECT real_weight, total_price FROM recycle_order WHERE id=%s AND deleted=0",
            (order_id,))
        assert row, f"order_id={order_id} 不存在"
        return float(row["real_weight"]), float(row["total_price"])

    def get_promoter_info(self, token):
        r = self.s.get(f"{APP_URL}/app-api/dist/promoter/info",
                       headers=self.app_headers(token), verify=False).json()
        self.assert_ok(r, "promoter info")
        return r["data"]

    def get_invite_config(self, level, star, rule_type, token):
        promote_type = 10 if rule_type == 1 else 20
        r = self.s.get(f"{APP_URL}/app-api/dist/rule/get", params={"promoteType": promote_type},
                       headers=self.app_headers(token), verify=False).json()
        self.assert_ok(r, "load invite config")
        for item in r["data"]:
            if item["level"] == level and item["star"] == star:
                return {
                    "first_invite_reward": item["firstInviteReward"],
                    "first_invite_team_reward_rate": item["firstInviteRewardRate"],
                    "second_invite_reward": item["secondInviteReward"],
                    "second_invite_team_reward_rate": item["secondInviteRewardRate"],
                }
        raise AssertionError(f"未匹配到 level={level} star={star} 的拉新配置")

    def get_invite_reward_sum(self, owner_id, account_type, source_type=10):
        row = self.db.fetch_one(
            "SELECT COALESCE(SUM(r.price), 0) as total "
            "FROM dist_commission_record r "
            "JOIN dist_commission_account a ON r.commission_account_id = a.id "
            "WHERE a.account_id=%s AND a.account_type=%s "
            "AND r.source_type=%s AND r.status=1 AND r.deleted=0 AND a.deleted=0",
            (owner_id, account_type, source_type))
        return int(row["total"])

    def assert_invite_reward(self, owner_id, account_type, expected, label="", timeout=15, source_type=10):
        time.sleep(5)  # 结算走 MQ，等待异步投递
        for _ in range(timeout * 2):
            actual = self.get_invite_reward_sum(owner_id, account_type, source_type)
            if actual == expected:
                print(f"  ✅ {label} 拉新奖励={actual}分")
                return
            time.sleep(0.5)
        actual = self.get_invite_reward_sum(owner_id, account_type, source_type)
        print(f"  ❌ {label} 拉新奖励不匹配: 预期={expected}, 实际={actual}")
        raise AssertionError(f"{label}: 预期={expected}, 实际={actual}")

    def get_team_commission_account_id(self, team_id):
        row = self.db.fetch_one(
            "SELECT id FROM dist_commission_account "
            "WHERE account_id=%s AND account_type=2 AND deleted=0",
            (team_id,))
        return int(row["id"]) if row else None

    def wait_personal_commission(self, order_id, promoter_id, timeout=20):
        time.sleep(5)  # 结算走 MQ，等待异步投递
        for _ in range(timeout * 2):
            row = self.db.fetch_one(
                "SELECT r.price FROM dist_commission_record r "
                "JOIN dist_commission_account a ON r.commission_account_id = a.id "
                "WHERE r.order_id=%s AND a.account_id=%s "
                "AND r.income_target_type=10 AND r.status=1 "
                "AND r.deleted=0 AND a.deleted=0",
                (order_id, promoter_id))
            if row:
                return float(row["price"])
            time.sleep(0.5)
        return None

    def wait_team_commission(self, order_id, team_account_id, timeout=40):
        """普通团队 income_target_type=20，企业团队=30，故不按类型过滤"""
        time.sleep(5)  # 结算走 MQ，等待异步投递
        for _ in range(timeout * 2):
            row = self.db.fetch_one(
                "SELECT price FROM dist_commission_record "
                "WHERE commission_account_id=%s AND order_id=%s "
                "AND status=1 AND deleted=0",
                (team_account_id, order_id))
            if row:
                return float(row["price"])
            time.sleep(0.5)
        return None

    def assert_commission(self, order_id, promoter_id, expected, label=""):
        actual = self.wait_personal_commission(order_id, promoter_id)
        if actual is None:
            record = self.db.fetch_one(
                "SELECT r.*, a.account_id FROM dist_commission_record r "
                "JOIN dist_commission_account a ON r.commission_account_id = a.id "
                "WHERE r.order_id=%s AND a.account_id=%s "
                "AND r.deleted=0 AND a.deleted=0",
                (order_id, promoter_id))
            print(f"  ❌ {label} 未找到已入账佣金记录")
            print(f"  完整记录: {record}")
            raise AssertionError(f"{label} 佣金未入账")
        if actual != expected:
            order = self.db.fetch_one(
                "SELECT real_weight, total_price FROM recycle_order WHERE id=%s AND deleted=0",
                (order_id,))
            print(f"  ❌ {label} 佣金不匹配")
            print(f"  理应入账: {expected}")
            print(f"  实际入账: {actual}")
            print(f"  订单信息: weight={order['real_weight']}, price={order['total_price']}")
            raise AssertionError(f"{label}: 预期={expected}, 实际={actual}")
        print(f"  ✅ {label} 佣金={actual}")

    def assert_team_commission(self, order_id, team_account_id, expected, label=""):
        actual = self.wait_team_commission(order_id, team_account_id)
        if actual is None:
            record = self.db.fetch_one(
                "SELECT * FROM dist_commission_record "
                "WHERE commission_account_id=%s AND order_id=%s AND deleted=0",
                (team_account_id, order_id))
            print(f"  ❌ {label} 未找到已入账团队佣金")
            print(f"  完整记录: {record}")
            raise AssertionError(f"{label} 团队佣金未入账")
        if actual != expected:
            order = self.db.fetch_one(
                "SELECT real_weight, total_price FROM recycle_order WHERE id=%s AND deleted=0",
                (order_id,))
            print(f"  ❌ {label} 团队佣金不匹配")
            print(f"  理应入账: {expected}")
            print(f"  实际入账: {actual}")
            print(f"  订单信息: weight={order['real_weight']}, price={order['total_price']}")
            raise AssertionError(f"{label}: 预期={expected}, 实际={actual}")
        print(f"  ✅ {label} 团队佣金={actual}")
