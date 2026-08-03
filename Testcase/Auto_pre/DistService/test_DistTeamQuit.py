"""退出团队：团员主动退团走 app /team/quit（团员专属），团长踢出走 admin"""
import datetime
import pytest
from config import APP_URL, ADMIN_URL
from Common.team_utils import TeamUtils

AUDITOR_ID = 2074701659722608641  # autotest 后台用户


class TestDistTeamQuit:

    @pytest.fixture(autouse=True)
    def _setup(self, api_session, login_tool, admin_token, db_client):
        self.tu = TeamUtils(api_session, login_tool, db_client, admin_token)
        self.s = api_session

    def _create_member(self, mobile_a, mobile_b):
        team_id, pid_a, token_a, _ = self.tu.become_team_leader(mobile_a)
        _, apply_id = self.tu.join_team(mobile_b, team_id)
        self.tu.audit_join(apply_id, token_a, status=20)
        return team_id, pid_a, token_a

    def _member_rel(self, team_id, pid_b):
        return self.tu.db.fetch_one(
            "SELECT id, team_id, promoter_id, team_user_type, join_type "
            "FROM dist_team_promoter_relation "
            "WHERE team_id=%s AND promoter_id=%s AND team_user_type=20 AND deleted=0",
            (team_id, pid_b))

    def _admin_quit(self, rel, quit_type):
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self.s.put(f"{ADMIN_URL}/admin-api/dist/team-promoter-relation/update", json={
            "id": rel["id"],
            "teamId": rel["team_id"],
            "promoterId": rel["promoter_id"],
            "joinType": rel["join_type"],
            "teamUserType": rel["team_user_type"],
            "sourceType": 20,
            "auditType": 0,
            "status": 20,
            "auditor": AUDITOR_ID,
            "joinTime": now,
            "quitTime": now,
            "quitType": quit_type,
            "settleStatus": 20,
            "rejectReason": "quit",
            "remark": "quit",
        }, headers=self.tu.admin_headers, verify=False).json()

    def _member_quit_app(self, mobile_b):
        """团员通过 app /team/quit 退团（业务上为团员专属接口）"""
        token_b = self.tu.login.app_login_for_promoter(mobile=mobile_b)
        return self.s.post(f"{APP_URL}/app-api/dist/team/quit",
                           json={"remark": "member quit"},
                           headers=self.tu.app_headers(token_b), verify=False).json()

    def test_member_quit(self):
        """团员主动退团（app /team/quit，团员专属接口）"""
        mobile_a = TeamUtils.gen_mobile()
        mobile_b = TeamUtils.gen_mobile()
        team_id, _, token_a = self._create_member(mobile_a, mobile_b)
        pid_b = self.tu.get_promoter_id_by_mobile(mobile_b)
        r = self._member_quit_app(mobile_b)
        self.tu.assert_ok(r, "member quit")
        assert r["data"].get("success") is True, f"退团 success={r['data'].get('success')} 应为true"
        print(f"  ✅ 团员通过 app /team/quit 退团成功")
        rel = self._member_rel(team_id, pid_b)
        row = self.tu.db.fetch_one(
            "SELECT * FROM dist_team_promoter_relation WHERE id=%s AND deleted=0", (rel["id"],))
        assert row["quit_time"] is not None, "quit_time 应为非空"
        assert row["settle_status"] == 20, f"退出后 settleStatus={row['settle_status']} 应为20"
        assert row["quit_type"] == 10, f"quitType={row['quit_type']} 应为10(主动退出)"

    def test_leader_kick(self):
        """团长踢出团员（admin 更新 quitType=20 + auditor）"""
        mobile_a = TeamUtils.gen_mobile()
        mobile_b = TeamUtils.gen_mobile()
        team_id, _, token_a = self._create_member(mobile_a, mobile_b)
        pid_b = self.tu.get_promoter_id_by_mobile(mobile_b)
        rel = self._member_rel(team_id, pid_b)
        self.tu.assert_ok(self._admin_quit(rel, 20), "kick")
        row = self.tu.db.fetch_one(
            "SELECT * FROM dist_team_promoter_relation WHERE id=%s AND deleted=0", (rel["id"],))
        assert row["quit_type"] == 20, f"quitType={row['quit_type']} 应为20(踢出)"
        assert row["quit_time"] is not None
        assert row["settle_status"] == 20

    def test_quit_after_commission_unchanged(self):
        """退出前已结算佣金不受影响"""
        mobile_a = TeamUtils.gen_mobile()
        mobile_b = TeamUtils.gen_mobile()
        mobile_c = TeamUtils.gen_mobile()
        team_id, pid_a, token_a, _ = self.tu.become_team_leader(mobile_a)
        pid_b = self.tu.become_promoter(mobile_b, promoter_id=pid_a)[0]
        _, apply_id = self.tu.join_team(mobile_b, team_id)
        self.tu.audit_join(apply_id, token_a, status=20)
        # C 绑定 B → 下单
        token_c = self.tu.login.app_login_for_promoter(mobile=mobile_c, promoter_id=pid_b)
        order_id = self.tu.settle_order(token_c, mobile_c)
        # 拿团队佣金账户 ID
        acc_id = self.tu.get_team_commission_account_id(team_id)
        # 退出前已有佣金
        team_comm = self.tu.wait_team_commission(order_id, acc_id, timeout=40)
        assert team_comm is not None, "退出前团队佣金应已入账"
        # 退出（app /team/quit，团员专属接口）
        r = self._member_quit_app(mobile_b)
        self.tu.assert_ok(r, "quit")
        # 历史佣金仍然存在
        comm_after = self.tu.wait_team_commission(order_id, acc_id)
        assert comm_after == team_comm, "退出后历史佣金不应变化"

    def test_quit_after_member_list(self):
        """退出后团队成员列表不再显示（产品确认后端 bug：退出成员仍显示，预期失败）"""
        mobile_a = TeamUtils.gen_mobile()
        mobile_b = TeamUtils.gen_mobile()
        team_id, _, token_a = self._create_member(mobile_a, mobile_b)
        pid_b = self.tu.get_promoter_id_by_mobile(mobile_b)
        r = self._member_quit_app(mobile_b)
        self.tu.assert_ok(r, "quit")
        r = self.s.get(f"{APP_URL}/app-api/dist/team/member/list",
                       headers=self.tu.app_headers(token_a),
                       params={"pageNo": 1, "pageSize": 20}, verify=False).json()
        self.tu.assert_ok(r, "member list")
        pids = [int(m["promoterId"]) for m in r["data"]["list"]]
        assert pid_b not in pids, "退出后仍显示在成员列表中"
        print("  ✅ 退出后 B 已不在成员列表")
