"""个人拉新奖励：校验一二级固定金额，无团队抽成"""
import time
import pytest
from Common.team_utils import TeamUtils


class TestDistInviteReward:

    @pytest.fixture(autouse=True)
    def _setup(self, api_session, login_tool, admin_token, db_client):
        self.tu = TeamUtils(api_session, login_tool, db_client, admin_token)

    def test_first_level_invite_reward(self):
        """A→B→B首单 → A 得 first_invite_reward (分)"""
        mobile_a = TeamUtils.gen_mobile()
        mobile_b = TeamUtils.gen_mobile()

        pid_a, token_a = self.tu.become_promoter(mobile_a)
        _, token_b = self.tu.become_promoter(mobile_b, promoter_id=pid_a)
        info_a = self.tu.get_promoter_info(token_a)
        cfg = self.tu.get_invite_config(info_a["level"], info_a["star"], 1, token_a)
        expected = int(cfg["first_invite_reward"])
        print(f"  预期一级拉新奖励: {expected}分")

        pid_b = self.tu.get_promoter_id_by_mobile(mobile_b)
        order_id = self.tu.settle_order(token_b, mobile_b)

        self.tu.assert_invite_reward(pid_a, account_type=1, expected=expected,
                                     label="A一级拉新")

    def test_second_level_invite_reward(self):
        """A→B→C→C首单 → B 一级, A 二级"""
        mobile_a = TeamUtils.gen_mobile()
        mobile_b = TeamUtils.gen_mobile()
        mobile_c = TeamUtils.gen_mobile()

        pid_a, token_a = self.tu.become_promoter(mobile_a)
        pid_b, token_b = self.tu.become_promoter(mobile_b, promoter_id=pid_a)
        _, token_c = self.tu.become_promoter(mobile_c, promoter_id=pid_b)
        info_a = self.tu.get_promoter_info(token_a)
        cfg = self.tu.get_invite_config(info_a["level"], info_a["star"], 1, token_a)
        exp_first = int(cfg["first_invite_reward"])
        exp_second = int(cfg["second_invite_reward"])
        print(f"  预期: B一级={exp_first}分, A二级={exp_second}分")

        order_id = self.tu.settle_order(token_c, mobile_c)

        self.tu.assert_invite_reward(pid_b, account_type=1, expected=exp_first,
                                     label="B一级拉新")
        self.tu.assert_invite_reward(pid_a, account_type=1, expected=exp_second,
                                     label="A二级拉新", source_type=11)

    def test_self_order_no_invite(self):
        """推广官自下单不产生拉新奖励"""
        mobile_a = TeamUtils.gen_mobile()
        pid_a, token_a = self.tu.become_promoter(mobile_a)
        time.sleep(1)
        before = self.tu.get_invite_reward_sum(pid_a, account_type=1)
        order_id = self.tu.settle_order(token_a, mobile_a)
        time.sleep(3)
        after = self.tu.get_invite_reward_sum(pid_a, account_type=1)
        assert after == before, f"自下单产生了拉新奖励: before={before} after={after}"
        print(f"  ✅ 自下单未产生拉新奖励 (sum={after})")
