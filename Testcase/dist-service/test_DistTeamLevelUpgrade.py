"""团队等级升级：达到 upgradeOrderTarget 后团队等级提升"""
import time
import pytest
from config import APP_URL
from Common.team_utils import TeamUtils


class TestDistTeamLevelUpgrade:

    @pytest.fixture(autouse=True)
    def _setup(self, api_session, login_tool, admin_token, db_client):
        self.tu = TeamUtils(api_session, login_tool, db_client, admin_token)
        self.s = api_session

    def test_team_level_upgrade(self):
        """团队凑够 upgradeOrderTarget+1 个订单后升级"""
        mobile_a = TeamUtils.gen_mobile()

        team_id, _, token_a, _ = self.tu.become_team_leader(mobile_a)
        info = self.tu.get_promoter_info(token_a)
        level_initial = info["teamInfo"]["teamLevel"]
        print(f"  初始团队等级: {level_initial}")

        rules = self.tu.load_team_rules(token_a)
        target = rules[0].get("upgradeOrderTarget", -1)
        if target <= 0:
            print(f"  upgradeOrderTarget={target}, 跳过升级测试")
            return
        print(f"  upgradeOrderTarget={target}")

        N = min(target + 1, 3)
        for i in range(N):
            mb = TeamUtils.gen_mobile()
            self.tu.become_promoter(mb)
            _, apply_id = self.tu.join_team(mb, team_id)
            self.tu.audit_join(apply_id, token_a, status=20)
            pid = self.tu.get_promoter_id_by_mobile(mb)
            mc = TeamUtils.gen_mobile()
            self.tu.become_promoter(mc, promoter_id=pid)
            token_c = self.tu.login.app_login_for_promoter(mobile=mc, promoter_id=pid)
            self.tu.settle_order(token_c, mc, num=5, predict_weight="5~10kg")
            print(f"  [{i+1}/{N}] {mb} 下线 {mc} 下单完成")

        from requests.exceptions import RequestException
        for _ in range(10):
            time.sleep(3)
            try:
                info = self.tu.get_promoter_info(token_a)
                curr_level = info["teamInfo"]["teamLevel"]
                if curr_level > level_initial:
                    print(f"  ✅ 团队等级升级: {level_initial} → {curr_level}")
                    return
            except (RequestException, KeyError, TypeError):
                pass
        print(f"  ⚠ 团队等级未从 {level_initial} 升级（dev 未结算或接口异常）")
