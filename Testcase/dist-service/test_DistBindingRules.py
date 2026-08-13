"""分销关系链规则：绑定、关闭推广官、拉新上限"""
import time
import pytest
from config import APP_URL, ADMIN_URL
from Common.login import Login

ID_CARD = "https://gips2.baidu.com/it/u=195724436,3554684702&fm=3028&app=3028&f=JPEG&fmt=auto?w=1280&h=960"


class TestDistBindingRules:
    """推广官绑定关系的各种规则校验"""

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
        self.mobiles = {
            "a": "156" + now_suffix,
            "b": "156" + str(int(now_suffix) + 1).zfill(8),
            "c": "156" + str(int(now_suffix) + 2).zfill(8),
            "d": "156" + str(int(now_suffix) + 3).zfill(8),
        }

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

    def _promoter_id(self, mobile):
        token = self.login.app_login_for_promoter(mobile=mobile)
        r = self.s.get(f"{APP_URL}/app-api/dist/promoter/info",headers=self._app_headers(token), verify=False).json()
        self._assert_ok(r, f"{mobile} info")
        pid = r["data"]["promoterId"]
        print(f"  [{mobile}] promoterId={pid}")
        return int(pid), token

    def _become_promoter(self, mobile, promoter_id=None):
        token = self.login.app_login_for_promoter(mobile=mobile, promoter_id=promoter_id)
        body = {"mobile": mobile, "provinceCode": "", "provinceName": "江苏省",
                "cityCode": "", "cityName": "苏州市", "districtCode": "", "districtName": "姑苏区",
                "promoteMode": 1, "hasMediaAccount": 1, "mediaAccountType": "",
                "mediaOtherDesc": "", "hasOfflineResource": 0, "offlineResource": "",
                "resourceOtherDesc": "", "hasSimilarExp": 1, "similarExp": "", "expOtherDesc": "",
                "mediaScreenshot": ""}
        r = self.s.post(f"{APP_URL}/app-api/dist/promoter/apply", json=body,headers=self._app_headers(token), verify=False).json()
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
        pid = r["data"]["promoterId"]
        assert int(pid) > 0
        return int(pid), token

    def _user_id_by_mobile(self, mobile):
        row = self._wait_db(
            "SELECT user_id FROM dist_promoter WHERE user_id="
            "(SELECT id FROM member_user WHERE mobile=%s) AND deleted=0", (mobile,),
            lambda r: True)
        return row["user_id"] if row else None

    def _get_parent_promoter(self, mobile):
        row = self._wait_db(
            "SELECT promoter_id FROM dist_promoter_user_relation "
            "WHERE user_id=(SELECT id FROM member_user WHERE mobile=%s) AND deleted=0",
            (mobile,), lambda r: True)
        return row["promoter_id"] if row else None

    def test_unbound_user_binds(self):
        print("\n=== 未绑定用户 + promoterId → 绑定 ===")
        pid_a, _ = self._become_promoter(self.mobiles["a"])
        self.login.app_login_for_promoter(mobile=self.mobiles["c"], promoter_id=pid_a)
        parent = self._get_parent_promoter(self.mobiles["c"])
        assert parent == pid_a, f"C 的上级应为 A(pid={pid_a})，实际={parent}"
        print(f"  ✅ C 已绑定到 A")

    def test_bound_user_no_override(self):
        print("\n=== 已绑定用户 + 新 promoterId → 不覆盖 ===")
        pid_a, _ = self._become_promoter(self.mobiles["a"])
        pid_b, _ = self._become_promoter(self.mobiles["b"], promoter_id=pid_a)
        self.login.app_login_for_promoter(mobile=self.mobiles["c"], promoter_id=pid_b)
        self.login.app_login_for_promoter(mobile=self.mobiles["c"], promoter_id=pid_a)
        parent = self._get_parent_promoter(self.mobiles["c"])
        assert parent == pid_b, f"C 的上级应仍是 B({pid_b})，不被 A 覆盖，实际={parent}"
        print(f"  ✅ C 仍绑定到 B，未被 A 覆盖")

    def test_closed_promoter_invite(self):
        print("\n=== 推广官关闭后 → 邀请码不可绑定 ===")
        pid_a, _ = self._become_promoter(self.mobiles["a"])
        uid_a = self._user_id_by_mobile(self.mobiles["a"])
        self.db.execute("UPDATE dist_promoter SET status=40 WHERE user_id=%s", (uid_a,))
        self.login.app_login_for_promoter(mobile=self.mobiles["c"], promoter_id=pid_a)
        parent = self._get_parent_promoter(self.mobiles["c"])
        assert parent is None, f"A 关闭后 C 不应绑定到 A, 实际={parent}"
        self.db.execute("UPDATE dist_promoter SET status=20 WHERE user_id=%s", (uid_a,))
        print(f"  ✅ A 关闭后邀请码不可绑定")

    def test_no_parent_normal_bind(self):
        print("\n=== 无上级推广官 + 下级绑定 → 正常 ===")
        pid_a, _ = self._become_promoter(self.mobiles["a"])
        pid_b, _ = self._become_promoter(self.mobiles["b"], promoter_id=pid_a)
        parent_b = self._get_parent_promoter(self.mobiles["b"])
        assert parent_b == pid_a, f"B 应绑定到 A, 实际={parent_b}"
        print(f"  ✅ B(无上级) → 绑定到 A(parent_promoter_id={parent_b})")

    def test_no_cycle_binding(self):
        print("\n=== 有上级推广官 + 下级 → 不形成循环 ===")
        pid_a, _ = self._become_promoter(self.mobiles["a"])
        pid_b, _ = self._become_promoter(self.mobiles["b"], promoter_id=pid_a)
        self.login.app_login_for_promoter(mobile=self.mobiles["c"], promoter_id=pid_b)
        parent_c = self._get_parent_promoter(self.mobiles["c"])
        parent_b = self._get_parent_promoter(self.mobiles["b"])
        assert parent_c == pid_b, f"C 应绑定到 B, 实际={parent_c}"
        assert parent_b == pid_a, f"B 应仍是 A 的下级, 实际={parent_b}"
        print(f"  ✅ B→A, C→B, 无循环")
