"""团队拉新奖励：校验一二级拉新的个人+团队分佣"""
import time
import pytest
from Common.team_utils import TeamUtils


class TestDistTeamInviteReward:

    @pytest.fixture(autouse=True)
    def _setup(self, api_session, login_tool, admin_token, db_client):
        self.tu = TeamUtils(api_session, login_tool, db_client, admin_token)

    def _calc_team_split(self, cfg, level=1):
        if level == 1:
            reward = int(cfg["first_invite_reward"])
            rate = float(cfg["first_invite_team_reward_rate"] or 0)
        else:
            reward = int(cfg["second_invite_reward"])
            rate = float(cfg["second_invite_team_reward_rate"] or 0)
        team = int(reward * rate)
        personal = reward - team
        return personal, team, reward

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
        personal_amt, team_amt, base = self._calc_team_split(cfg, level=1)
        print(f"  一级拉新: base={base}, 团员得={personal_amt}, 团队得={team_amt}")

        token_c = self.tu.login.app_login_for_promoter(mobile=mobile_c, promoter_id=pid_b)
        order_id = self.tu.settle_order(token_c, mobile_c)
        time.sleep(2)

        self.tu.assert_invite_reward(pid_b, account_type=1, expected=personal_amt,
                                     label="B个人一级拉新")
        self.tu.assert_invite_reward(team_id, account_type=2, expected=team_amt,
                                     label="A团队一级拉新")

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
        p1, t1, b1 = self._calc_team_split(cfg, level=1)
        p2, t2, b2 = self._calc_team_split(cfg, level=2)
        print(f"  一级拉新: base={b1}, 团员得={p1}, 团队得={t1}")
        print(f"  二级拉新: base={b2}, 团员得={p2}, 团队得={t2}")

        token_d = self.tu.login.app_login_for_promoter(mobile=mobile_d, promoter_id=pid_c)
        order_id = self.tu.settle_order(token_d, mobile_d)
        time.sleep(2)

        self.tu.assert_invite_reward(pid_c, account_type=1, expected=p1,
                                     label="C个人一级拉新")
        self.tu.assert_invite_reward(team_id, account_type=2, expected=t1,
                                     label="A团队一级拉新")
        self.tu.assert_invite_reward(pid_b, account_type=1, expected=p2,
                                     label="B个人二级拉新", source_type=11)
        self.tu.assert_invite_reward(team_id, account_type=2, expected=t1 + t2,
                                     label="A团队总拉新")

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

        order_1 = self.tu.settle_order(token_c, mobile_c)
        time.sleep(2)

        info_a = self.tu.get_promoter_info(token_a)
        cfg = self.tu.get_invite_config(info_a["level"], info_a["star"], 2, token_a)
        personal_amt, team_amt, _ = self._calc_team_split(cfg, level=1)

        self.tu.assert_invite_reward(pid_b, account_type=1, expected=personal_amt,
                                     label="B首次拉新")
        self.tu.assert_invite_reward(team_id, account_type=2, expected=team_amt,
                                     label="团队首次拉新")

        before_b = self.tu.get_invite_reward_sum(pid_b, account_type=1)
        before_t = self.tu.get_invite_reward_sum(team_id, account_type=2)

        order_2 = self.tu.settle_order(token_c, mobile_c, num=3)
        time.sleep(3)

        after_b = self.tu.get_invite_reward_sum(pid_b, account_type=1)
        after_t = self.tu.get_invite_reward_sum(team_id, account_type=2)
        assert after_b == before_b, f"第二次下单后 B 拉新奖励变化: {before_b}→{after_b}"
        assert after_t == before_t, f"第二次下单后团队拉新奖励变化: {before_t}→{after_t}"
        print(f"  ✅ 两次下单后拉新奖励未重复发放")
