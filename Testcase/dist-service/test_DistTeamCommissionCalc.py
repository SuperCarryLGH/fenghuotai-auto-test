"""团队分佣：校验个人佣金 + 团队佣金同时入账"""
import pytest
from config import APP_URL
from Common.team_utils import TeamUtils


class TestDistTeamCommissionCalc:

    @pytest.fixture(autouse=True)
    def _setup(self, api_session, login_tool, admin_token, db_client):
        self.tu = TeamUtils(api_session, login_tool, db_client, admin_token)
        self.s = api_session

    def test_team_commission_basic(self):
        """
        A 团长 → B 入团 → C 绑定 B 下单
        校验: B 个人佣金 + A 团队佣金
        """
        mobile_a = TeamUtils.gen_mobile()
        mobile_b = TeamUtils.gen_mobile()
        mobile_c = TeamUtils.gen_mobile()

        # 1. A 成为团长
        team_id, pid_a, token_a, _ = self.tu.become_team_leader(mobile_a)

        # 2. B 绑定 A 成为推广员 → 入团（团队佣金来自 A 的二级佣金，需 A 在链上）
        pid_b = self.tu.become_promoter(mobile_b, promoter_id=pid_a)[0]
        _, apply_id = self.tu.join_team(mobile_b, team_id)
        self.tu.audit_join(apply_id, token_a, status=20)

        # 3. C 绑定 B → 下单
        token_c = self.tu.login.app_login_for_promoter(mobile=mobile_c, promoter_id=pid_b)
        before_b = self.tu.get_wallet_balance(pid_b, 1)
        before_t = self.tu.get_wallet_balance(team_id, 2)
        order_id = self.tu.settle_order(token_c, mobile_c)
        real_weight, total_price = self.tu.get_order_data(order_id)

        # setup 身份日志
        print(f"  A(团长): mobile={mobile_a}, promoter_id={pid_a}, team_id={team_id}")
        print(f"  B(团员): mobile={mobile_b}, promoter_id={pid_b}")
        print(f"  C(买家): mobile={mobile_c}, order_id={order_id}")
        self.tu.dump_order_context("test_team_commission_basic", order_id, team_id, pid_b, mobile_b)

        # 4. 加载规则
        rules = self.tu.load_team_rules(token_a)
        info = self.tu.get_promoter_info(token_a)
        level, star = info["level"], info["star"]
        _, detail = self.tu.match_rule_detail(rules, level, star, real_weight)

        # 5. 计算预期（个人逻辑：一级给B个人，二级给A，A有团队则分成给团队）
        expected_personal, expected_personal_l2, expected_team = self.tu.calc_team_split(detail, total_price)
        print(f"  weight={real_weight}, price={total_price}")
        print(f"  预期个人一级={expected_personal}, 团队二级={expected_team}")

        # 6-7. 钱包金额校验（全给团队：B 个人无收益，团队全额入账）
        self.tu.assert_wallet_delta(team_id, 2, before_t,
                                    expected_personal + expected_team, label="A团队")
        self.tu.assert_wallet_delta(pid_b, 1, before_b, 0, label="B个人")

        # 8. APP 侧校验：A 团队订单列表可见本单佣金（全给团队下 B 个人无佣金）
        team_comm = self._find_order_commission(token_a, order_id, 20)
        assert team_comm is not None and team_comm > 0, "A 团队订单列表查不到本单佣金"
        print(f"  APP 团队订单列表可见本单佣金={team_comm}")

    def _find_order_commission(self, token, order_id, promote_type):
        """APP stats/order-list 里找本单的 orderCommission"""
        r = self.s.get(f"{APP_URL}/app-api/dist/stats/order-list",
                       headers=self.tu.app_headers(token),
                       params={"promoteType": promote_type, "pageNo": 1, "pageSize": 20}, verify=False).json()
        self.tu.assert_ok(r, f"order list promoteType={promote_type}")
        for o in r["data"]["list"]:
            if int(o["orderId"]) == int(order_id):
                return int(o.get("orderCommission", 0))
        return None

    def test_team_commission_order_list(self):
        """APP 团队订单列表能看到本单团队佣金"""
        mobile_a = TeamUtils.gen_mobile()
        mobile_b = TeamUtils.gen_mobile()
        mobile_c = TeamUtils.gen_mobile()
        team_id, pid_a, token_a, _ = self.tu.become_team_leader(mobile_a)
        pid_b = self.tu.become_promoter(mobile_b, promoter_id=pid_a)[0]
        _, apply_id = self.tu.join_team(mobile_b, team_id)
        self.tu.audit_join(apply_id, token_a, status=20)
        token_c = self.tu.login.app_login_for_promoter(mobile=mobile_c, promoter_id=pid_b)
        order_id = self.tu.settle_order(token_c, mobile_c)
        team_acc_id = self.tu.get_team_commission_account_id(team_id)
        assert self.tu.wait_team_commission(order_id, team_acc_id, timeout=40) is not None, "团队佣金未入账"
        team_comm = self._find_order_commission(token_a, order_id, 20)
        assert team_comm is not None and team_comm > 0, "团队订单列表查不到本单佣金"
        print(f"  ✅ APP 团队订单列表可见本单佣金={team_comm}")
