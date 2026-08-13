"""团队拉新奖励：校验一二级拉新的个人+团队分佣"""
import time
import pytest
from Common.team_utils import TeamUtils


class TestDistTeamInviteReward:

    @pytest.fixture(autouse=True)
    def _setup(self, api_session, login_tool, admin_token, db_client):
        self.tu = TeamUtils(api_session, login_tool, db_client, admin_token)

    def test_team_invite_first_level(self):
        """A(团长)→B(团员)→B拉C→C首单 → B个人一级 + 团队一级抽成"""
        mobile_a = TeamUtils.gen_mobile()
        mobile_b = TeamUtils.gen_mobile()
        mobile_c = TeamUtils.gen_mobile()

        team_id, pid_a, token_a, _ = self.tu.become_team_leader(mobile_a)
        token_b, apply_id = self.tu.join_team(mobile_b, team_id)
        self.tu.audit_join(apply_id, token_a, status=20)
        pid_b = self.tu.get_promoter_id_by_mobile(mobile_b)

        info_a = self.tu.get_promoter_info(token_a)
        cfg = self.tu.get_invite_config(info_a["level"], info_a["star"], 2, token_a)
        base = int(cfg["first_invite_reward"])
        print(f"  一级拉新: base={base}, 全给团队下 团队得={base}")

        before_b = self.tu.get_wallet_balance(pid_b, 1)
        before_t = self.tu.get_wallet_balance(team_id, 2)
        token_c = self.tu.login.app_login_for_promoter(mobile=mobile_c, promoter_id=pid_b)
        order_id = self.tu.settle_order(token_c, mobile_c)

        self.tu.assert_wallet_delta(pid_b, 1, before_b, 0, label="B个人一级拉新")
        self.tu.assert_wallet_delta(team_id, 2, before_t, base, label="A团队一级拉新")

    def test_team_invite_second_level(self):
        """A(团长)→B(团员)→C(被B拉)→C拉D→D首单
        C一级个人+团队, B二级个人+团队"""
        mobile_a = TeamUtils.gen_mobile()
        mobile_b = TeamUtils.gen_mobile()
        mobile_c = TeamUtils.gen_mobile()
        mobile_d = TeamUtils.gen_mobile()

        team_id, pid_a, token_a, _ = self.tu.become_team_leader(mobile_a)
        _, apply_id = self.tu.join_team(mobile_b, team_id)
        self.tu.audit_join(apply_id, token_a, status=20)
        pid_b = self.tu.get_promoter_id_by_mobile(mobile_b)
        # C 绑定 B 成为推广员 → 入团（二级拉新需 C 是 B 的下线）
        pid_c = self.tu.become_promoter(mobile_c, promoter_id=pid_b)[0]
        _, apply_id = self.tu.join_team(mobile_c, team_id)
        self.tu.audit_join(apply_id, token_a, status=20)

        info_a = self.tu.get_promoter_info(token_a)
        cfg = self.tu.get_invite_config(info_a["level"], info_a["star"], 2, token_a)
        b1 = int(cfg["first_invite_reward"])
        b2 = int(cfg["second_invite_reward"])
        print(f"  一级拉新 base={b1}, 二级拉新 base={b2}, 全给团队下团队总得={b1 + b2}")

        before_c = self.tu.get_wallet_balance(pid_c, 1)
        before_b = self.tu.get_wallet_balance(pid_b, 1)
        before_t = self.tu.get_wallet_balance(team_id, 2)
        token_d = self.tu.login.app_login_for_promoter(mobile=mobile_d, promoter_id=pid_c)
        order_id = self.tu.settle_order(token_d, mobile_d)

        self.tu.assert_wallet_delta(pid_c, 1, before_c, 0, label="C个人一级拉新")
        self.tu.assert_wallet_delta(pid_b, 1, before_b, 0, label="B个人二级拉新")
        self.tu.assert_wallet_delta(team_id, 2, before_t, b1 + b2, label="A团队总拉新")

    def test_team_invite_once_per_person(self):
        """每人首单只触发一次拉新奖励，后续不下发"""
        mobile_a = TeamUtils.gen_mobile()
        mobile_b = TeamUtils.gen_mobile()
        mobile_c = TeamUtils.gen_mobile()

        team_id, pid_a, token_a, _ = self.tu.become_team_leader(mobile_a)
        _, apply_id = self.tu.join_team(mobile_b, team_id)
        self.tu.audit_join(apply_id, token_a, status=20)
        pid_b = self.tu.get_promoter_id_by_mobile(mobile_b)
        token_c = self.tu.login.app_login_for_promoter(mobile=mobile_c, promoter_id=pid_b)

        before_b = self.tu.get_wallet_balance(pid_b, 1)
        before_t = self.tu.get_wallet_balance(team_id, 2)
        token_c = self.tu.login.app_login_for_promoter(mobile=mobile_c, promoter_id=pid_b)
        order_1 = self.tu.settle_order(token_c, mobile_c)
        time.sleep(2)

        info_a = self.tu.get_promoter_info(token_a)
        cfg = self.tu.get_invite_config(info_a["level"], info_a["star"], 2, token_a)
        base = int(cfg["first_invite_reward"])

        self.tu.assert_wallet_delta(pid_b, 1, before_b, 0, label="B首次拉新")
        # 团队拉新用拉新记录和校验（拉新在 B 入团/绑定阶段已入账，钱包窗口对不上）
        self.tu.assert_invite_reward(team_id, account_type=2, expected=base, label="团队首次拉新")

        # 第二次下单：拉新不重复发放（用拉新记录和校验，订单佣金会重复不计入）
        before_inv_b = self.tu.get_invite_reward_sum(pid_b, account_type=1)
        before_inv_t = self.tu.get_invite_reward_sum(team_id, account_type=2)

        order_2 = self.tu.settle_order(token_c, mobile_c, num=3)
        time.sleep(3)

        after_inv_b = self.tu.get_invite_reward_sum(pid_b, account_type=1)
        after_inv_t = self.tu.get_invite_reward_sum(team_id, account_type=2)
        assert after_inv_b == before_inv_b, f"第二次下单后 B 拉新奖励变化: {before_inv_b}→{after_inv_b}"
        assert after_inv_t == before_inv_t, f"第二次下单后团队拉新奖励变化: {before_inv_t}→{after_inv_t}"
        print(f"  ✅ 两次下单后拉新奖励未重复发放")
