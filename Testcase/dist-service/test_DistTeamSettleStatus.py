"""settleStatus=20 成员不参与分佣：不影响团长自身的二级团队佣金"""
import pytest
from config import APP_URL, ADMIN_URL
from Common.team_utils import TeamUtils


class TestDistTeamSettleStatus:

    @pytest.fixture(autouse=True)
    def _setup(self, api_session, login_tool, admin_token, db_client):
        self.tu = TeamUtils(api_session, login_tool, db_client, admin_token)
        self.s = api_session

    def test_team_commission_independent_of_member_settle_status(self):
        """
        团队佣金 = 团长 A 自己的二级佣金（链 C←B←A）。
        成员 B 的 settleStatus=20 不影响 A 的团队佣金入账，也不影响历史佣金。
        """
        mobile_a = TeamUtils.gen_mobile()
        mobile_b = TeamUtils.gen_mobile()
        mobile_c1 = TeamUtils.gen_mobile()
        mobile_c2 = TeamUtils.gen_mobile()

        team_id, pid_a, token_a, _ = self.tu.become_team_leader(mobile_a)
        # B 绑定 A 成为推广员 → 入团
        pid_b = self.tu.become_promoter(mobile_b, promoter_id=pid_a)[0]
        _, apply_id = self.tu.join_team(mobile_b, team_id)
        self.tu.audit_join(apply_id, token_a, status=20)
        team_acc_id = self.tu.get_team_commission_account_id(team_id)
        assert team_acc_id is not None

        # Phase 1: C1 绑定 B → 下单 → 团队佣金入账
        token_c1 = self.tu.login.app_login_for_promoter(mobile=mobile_c1, promoter_id=pid_b)
        order_id_1 = self.tu.settle_order(token_c1, mobile_c1)
        comm1 = self.tu.wait_team_commission(order_id_1, team_acc_id, timeout=40)
        assert comm1 is not None, "Ph1: 应有团队佣金"
        print(f"  ✅ Ph1 C1 下单: 团队佣金={comm1}")

        # Phase 2: 改 B settleStatus=20
        rel = self.tu.db.fetch_one(
            "SELECT id, join_time FROM dist_team_promoter_relation WHERE team_id=%s AND promoter_id=%s AND deleted=0",
            (team_id, pid_b))
        join_time = rel["join_time"].strftime("%Y-%m-%d %H:%M:%S") if rel["join_time"] else ""
        self.tu.assert_ok(self.s.put(f"{ADMIN_URL}/admin-api/dist/team-promoter-relation/update", json={
            "id": rel["id"], "teamId": team_id, "promoterId": pid_b,
            "settleStatus": 20, "status": 20, "teamUserType": 20,
            "joinType": 10, "sourceType": 20, "auditType": 0,
            "joinTime": join_time,
            "auditor": 2074701659722608641, "rejectReason": "settle off", "remark": "settle off",
        }, headers=self.tu.admin_headers, verify=False).json(), "set settleStatus=20")

        # Phase 3: C2 绑定 B → 下单 → A 团队佣金仍入账（是 A 自己的二级佣金，与 B 状态无关）
        token_c2 = self.tu.login.app_login_for_promoter(mobile=mobile_c2, promoter_id=pid_b)
        order_id_2 = self.tu.settle_order(token_c2, mobile_c2)
        comm2 = self.tu.wait_team_commission(order_id_2, team_acc_id, timeout=40)
        assert comm2 is not None, "Ph3: 成员 settleStatus=20 不应影响团长二级团队佣金"
        print(f"  ✅ Ph3 C2 下单: 团队佣金={comm2}（成员 settleStatus=20 不影响团长自身佣金）")

        # Phase 4: Ph1 的历史佣金不被影响
        comm1_after = self.tu.wait_team_commission(order_id_1, team_acc_id)
        assert comm1_after == comm1, "历史佣金不应变化"
        print(f"  ✅ Ph4: 历史佣金不变")
