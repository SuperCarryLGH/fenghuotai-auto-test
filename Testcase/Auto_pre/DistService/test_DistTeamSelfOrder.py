"""团员自下单：买家本人无个人佣金，上级（团长）得一级佣金进团队（产品确认后端逻辑）"""
import pytest
from Common.team_utils import TeamUtils


class TestDistTeamSelfOrder:

    @pytest.fixture(autouse=True)
    def _setup(self, api_session, login_tool, admin_token, db_client):
        self.tu = TeamUtils(api_session, login_tool, db_client, admin_token)
        self.s = api_session

    def test_member_self_order_upline_team_commission(self):
        """团员自下单：买家 B 本人无个人佣金；上级 A 得一级佣金进团队"""
        mobile_a = TeamUtils.gen_mobile()
        mobile_b = TeamUtils.gen_mobile()

        team_id, pid_a, token_a, _ = self.tu.become_team_leader(mobile_a)
        # B 绑定 A 成为推广员 → 入团
        pid_b = self.tu.become_promoter(mobile_b, promoter_id=pid_a)[0]
        _, apply_id = self.tu.join_team(mobile_b, team_id)
        self.tu.audit_join(apply_id, token_a, status=20)
        team_acc_id = self.tu.get_team_commission_account_id(team_id)
        assert team_acc_id is not None

        # B 自己下单
        token_b = self.tu.login.app_login_for_promoter(mobile=mobile_b)
        order_id = self.tu.settle_order(token_b, mobile_b)

        # 1. 正断言：上级 A 得一级佣金进团队（产品确认后端逻辑正常）
        team_comm = self.tu.wait_team_commission(order_id, team_acc_id, timeout=40)
        assert team_comm is not None, "上级 A 应得一级佣金进团队"
        print(f"  ✅ 上级 A 团队佣金={team_comm}（团员自下单正常给团长产生佣金）")

        # 2. 负断言：买家 B 本人无个人佣金（买家不从自己订单获利）
        personal = self.tu.wait_personal_commission(order_id, pid_b, timeout=10)
        assert personal is None, f"买家 B 自己下单不应有个人佣金, 实际={personal}"
        print(f"  ✅ 买家 B 自下单无个人佣金")
