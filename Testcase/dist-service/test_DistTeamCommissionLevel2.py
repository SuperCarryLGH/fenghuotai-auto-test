"""二级团队佣金：校验多层团队分佣链"""
import pytest
from Common.team_utils import TeamUtils


class TestDistTeamCommissionLevel2:

    @pytest.fixture(autouse=True)
    def _setup(self, api_session, login_tool, admin_token, db_client):
        self.tu = TeamUtils(api_session, login_tool, db_client, admin_token)

    def test_level2_team_commission(self):
        """
        A 团长 → B 入团 → C 绑定 B → D 绑定 C → D 下单
        校验: C 个人一级佣金, B 个人二级佣金, A 团队一级佣金
        """
        mobile_a = TeamUtils.gen_mobile()
        mobile_b = TeamUtils.gen_mobile()
        mobile_c = TeamUtils.gen_mobile()
        mobile_d = TeamUtils.gen_mobile()

        # A 团长
        team_id, pid_a, token_a, _ = self.tu.become_team_leader(mobile_a)
        # B 入团
        _, apply_id = self.tu.join_team(mobile_b, team_id)
        self.tu.audit_join(apply_id, token_a, status=20)
        pid_b = self.tu.get_promoter_id_by_mobile(mobile_b)
        # C 绑定 B 成为推广员
        pid_c = self.tu.become_promoter(mobile_c, promoter_id=pid_b)[0]
        # D 绑定 C → 下单
        token_d = self.tu.login.app_login_for_promoter(mobile=mobile_d, promoter_id=pid_c)
        before_b = self.tu.get_wallet_balance(pid_b, 1)
        before_t = self.tu.get_wallet_balance(team_id, 2)
        order_id = self.tu.settle_order(token_d, mobile_d)
        real_weight, total_price = self.tu.get_order_data(order_id)

        # 加载规则
        rules = self.tu.load_team_rules(token_a)
        info = self.tu.get_promoter_info(token_a)
        _, detail = self.tu.match_rule_detail(rules, info["level"], info["star"], real_weight)

        # 计算预期（个人逻辑：一级给C，二级给B；B无团队则二级全归B个人）
        rm = detail["rewardMode"]
        if rm == 1:
            exp_first = detail["firstFixedReward"]
            exp_second = detail["secondFixedReward"]
        else:
            exp_first = total_price * detail["firstOrderRate"]
            exp_second = total_price * detail["secondOrderRate"]
        print(f"  weight={real_weight}, price={total_price}")
        print(f"  预期: C一级={exp_first}, B二级={exp_second}")

        # C 个人一级佣金（C 非团员，保留个人）
        self.tu.assert_commission(order_id, pid_c, exp_first, "C个人一级")
        # B 个人二级佣金（B 是团员，全给团队下无个人收益）
        self.tu.assert_wallet_delta(pid_b, 1, before_b, 0, label="B个人")
        # A 团队佣金（全给团队：B 的二级进团队）
        self.tu.assert_wallet_delta(team_id, 2, before_t, exp_second, label="A团队")
