"""老用户/已注册用户不能被拉新 — 双表校验"""
import time

import pytest
from config import APP_URL, ADMIN_URL
from Common.login import Login

ID_CARD = "https://gips2.baidu.com/it/u=195724436,3554684702&fm=3028&app=3028&f=JPEG&fmt=auto?w=1280&h=960"


class TestDistOldUserNoBind:
    """老用户带 promoterId 登录，不应绑定上下级关系"""

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

    def _become_promoter(self, mobile):
        token = self.login.app_login_for_promoter(mobile=mobile)
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
        return int(r["data"]["promoterId"]), token

    def _assert_no_bind(self, mobile):
        """dist_promoter_user_relation 校验：该用户未绑定任何上级"""
        row = self.db.fetch_one(
            "SELECT COUNT(*) as cnt FROM dist_promoter_user_relation "
            "WHERE user_id=(SELECT id FROM member_user WHERE mobile=%s) AND deleted=0",
            (mobile,))
        cnt = int(row["cnt"]) if row and row.get("cnt") is not None else 0
        assert cnt == 0, f"{mobile} 应有 0 条绑定，实际={cnt}"

    def _assert_bound(self, mobile, expected_promoter_id):
        """dist_promoter_user_relation 校验：promoter↔user 绑定（异步，最多等 15 秒）"""
        row = None
        for i in range(30):
            row = self.db.fetch_one(
                "SELECT COUNT(*) as cnt FROM dist_promoter_user_relation "
                "WHERE promoter_id=%s AND user_id=(SELECT id FROM member_user WHERE mobile=%s) AND deleted=0",
                (expected_promoter_id, mobile))
            if row and row["cnt"] >= 1:
                break
            time.sleep(0.5)
        assert row and row["cnt"] >= 1, \
            f"{mobile} 应绑定到 promoter({expected_promoter_id})，实际={row['cnt'] if row else 0}"

    # ============================================================
    # Case 1: 老用户（有订单记录）— 不能被拉新
    # ============================================================
    @pytest.mark.smoke
    def test_old_user_with_orders_no_bind(self):
        print(f"\n=== Case 1: 老用户(15617637160,有订单) — 不能被拉新 ===")
        pid_a, _ = self._become_promoter(self.mobile_a)
        self.login.app_login_for_promoter(mobile="15617637160", promoter_id=pid_a)
        self._assert_no_bind("15617637160")
        print("  ✅ 老用户(有订单)未被绑定")

    # ============================================================
    # Case 2: 已注册无订单用户 — 不能被拉新
    # ============================================================
    def test_registered_user_no_orders_no_bind(self):
        print(f"\n=== Case 2: 已注册无订单用户 — 不能被拉新 ===")
        pid_a, _ = self._become_promoter(self.mobile_a)
        mobile_b = "156" + str(int(time.time() * 1000))[-8:]
        self.login.app_login(mobile=mobile_b)
        self.login.app_login_for_promoter(mobile=mobile_b, promoter_id=pid_a)
        self._assert_no_bind(mobile_b)
        print(f"  ✅ 已注册用户({mobile_b})未被绑定")

    # ============================================================
    # Case 3: 全新用户 — 正常绑定（对照组）
    # ============================================================
    def test_new_user_normal_bind(self):
        print(f"\n=== Case 3: 全新用户 — 正常绑定 ===")
        pid_a, _ = self._become_promoter(self.mobile_a)
        mobile_c = "156" + str(int(time.time() * 1000))[-8:]
        self.login.app_login_for_promoter(mobile=mobile_c, promoter_id=pid_a)
        self._assert_bound(mobile_c, pid_a)
        print(f"  ✅ 全新用户({mobile_c})正常绑定到 A({pid_a})")
