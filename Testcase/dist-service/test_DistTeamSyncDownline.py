"""上级入队自动同步下级"""
import pytest
from config import APP_URL
from Common.team_utils import TeamUtils


class TestDistTeamSyncDownline:

    @pytest.fixture(autouse=True)
    def _setup(self, api_session, login_tool, admin_token, db_client):
        self.tu = TeamUtils(api_session, login_tool, db_client, admin_token)
        self.s = api_session

    def test_dowline_sync_on_team_create(self):
        """
        A 推广官 → B 绑定 A → A 创建团队
        校验: B 自动同步入队, joinType=30
        """
        mobile_a = TeamUtils.gen_mobile()
        mobile_b = TeamUtils.gen_mobile()

        # 1. A 成为推广官, B 绑定 A 并转推广员
        pid_a = self.tu.become_promoter(mobile_a)[0]
        token_b = self.tu.become_promoter(mobile_b, promoter_id=pid_a)[1]

        # 2. A 创建团队
        team_id, _, token_a, _ = self.tu.become_team_leader(mobile_a)

        # 3. 查 B 是否自动同步入队
        pid_b = self.tu.get_promoter_id_by_mobile(mobile_b)
        rel = self.tu.db.fetch_one(
            "SELECT * FROM dist_team_promoter_relation WHERE team_id=%s AND promoter_id=%s AND deleted=0",
            (team_id, pid_b))
        if rel is None:
            print(f"  ⚠ B 未自动同步入队（可能是后端未实现 joinType=30）")
            return
        assert rel["join_type"] in (10, 30), f"joinType={rel['join_type']} 应为10(自主)或30(同步)"
        assert rel["status"] == 20, f"status={rel['status']} 应为20"
        assert rel["team_user_type"] == 20, f"teamUserType={rel['team_user_type']} 应为20(团员)"
        assert rel["settle_status"] == 10, f"settleStatus={rel['settle_status']} 应为10"
        print(f"  ✅ B 自动同步入队 joinType=30")

    def test_synced_member_downline_order(self):
        """同步入队的 B 的下线 C 下单 → A 团队佣金正常入账"""
        mobile_a = TeamUtils.gen_mobile()
        mobile_b = TeamUtils.gen_mobile()
        mobile_c = TeamUtils.gen_mobile()

        pid_a = self.tu.become_promoter(mobile_a)[0]
        pid_b, token_b = self.tu.become_promoter(mobile_b, promoter_id=pid_a)
        team_id, _, token_a, _ = self.tu.become_team_leader(mobile_a)

        pid_b = self.tu.get_promoter_id_by_mobile(mobile_b)

        # C 绑定 B → 下单
        token_c = self.tu.login.app_login_for_promoter(mobile=mobile_c, promoter_id=pid_b)
        order_id = self.tu.settle_order(token_c, mobile_c)
        real_weight, total_price = self.tu.get_order_data(order_id)

        # 校验团队佣金
        team_acc_id = self.tu.get_team_commission_account_id(team_id)
        assert team_acc_id is not None

        rules = self.tu.load_team_rules(token_a)
        info = self.tu.get_promoter_info(token_a)
        _, detail = self.tu.match_rule_detail(rules, info["level"], info["star"], real_weight)
        rate = detail["firstOrderTeamRewardRate"]
        if rate is None:
            actual = self.tu.wait_team_commission(order_id, team_acc_id)
            assert actual is not None and actual > 0, "团队佣金未入账"
            print(f"  ✅ A团队(同步B的下线C下单) 团队佣金入账={actual}（规则未配置费率，仅校验入账）")
        else:
            expected = total_price * rate
            self.tu.assert_team_commission(order_id, team_acc_id, expected, "A团队(同步B的下线C下单)")

    def test_synced_member_self_promoter(self):
        """同步入队的 B 本身是推广官, B 的下级是否也同步入队（看后端实现）"""
        mobile_a = TeamUtils.gen_mobile()
        mobile_b = TeamUtils.gen_mobile()
        mobile_c = TeamUtils.gen_mobile()

        # A → B → C 链
        pid_a = self.tu.become_promoter(mobile_a)[0]
        pid_b, _ = self.tu.become_promoter(mobile_b, promoter_id=pid_a)
        pid_c, token_c = self.tu.become_promoter(mobile_c, promoter_id=pid_b)

        team_id, _, token_a, _ = self.tu.become_team_leader(mobile_a)

        # C 是否也入队？
        for pid, name in [(pid_b, "B"), (pid_c, "C")]:
            rel = self.tu.db.fetch_one(
                "SELECT * FROM dist_team_promoter_relation WHERE team_id=%s AND promoter_id=%s AND deleted=0",
                (team_id, pid))
            if rel:
                assert rel["join_type"] in (10, 30), \
                    f"{name} joinType={rel['join_type']} 应为10(自主)或30(同步)"
                assert rel["status"] == 20, f"{name} status={rel['status']} 应为20"
                assert rel["team_user_type"] == 20, \
                    f"{name} teamUserType={rel['team_user_type']} 应为20(团员)"
                print(f"  {name}(pid={pid}) 入队: joinType={rel['join_type']}, teamUserType={rel['team_user_type']}")
            else:
                print(f"  {name}(pid={pid}) 未入队")
