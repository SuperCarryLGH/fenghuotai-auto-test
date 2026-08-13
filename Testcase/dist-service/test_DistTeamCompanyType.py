"""企业团队 vs 普通团队：企业认证流程 + 分佣"""
import pytest
from config import APP_URL, ADMIN_URL
from Common.team_utils import TeamUtils


class TestDistTeamCompanyType:

    @pytest.fixture(autouse=True)
    def _setup(self, api_session, login_tool, admin_token, db_client):
        self.tu = TeamUtils(api_session, login_tool, db_client, admin_token)
        self.s = api_session

    def test_company_team_apply(self):
        """申请企业团队 + 企业认证 + 审核通过"""
        mobile_a = TeamUtils.gen_mobile()

        # 1. 推广官申请企业团队
        pid_a, token_a = self.tu.become_promoter(mobile_a)
        r = self.s.post(f"{APP_URL}/app-api/dist/team/apply", json={
            "teamType": 2, "teamName": f"company_{mobile_a[-4:]}",
            "mobile": mobile_a, "address": "企业地址",
            "socialAccount": "微信,抖音", "groupChannel": "微信社群",
        }, headers=self.tu.app_headers(token_a), verify=False).json()
        self.tu.assert_ok(r, "company team apply")
        apply_id = r["data"]["applyId"]

        # 2. 企业认证提交
        r = self.s.post(f"{APP_URL}/app-api/dist/team/company-auth", json={
            "companyName": "测试企业有限公司", "creditCode": "91320594MA1M9K2Q3Y",
            "businessLicenseUrl": "https://example.com/license.jpg",
            "legalPersonName": "张三", "legalPersonIdCard": "110101199003071234",
            "legalIdCardFront": "https://example.com/id_front.jpg",
            "legalIdCardBack": "https://example.com/id_back.jpg",
            "businessScope": "再生资源回收", "businessValidDate": "2099-12-31",
        }, headers=self.tu.app_headers(token_a), verify=False).json()
        self.tu.assert_ok(r, "company auth")
        assert r["data"]["companyAuthStatus"] in (0, 1, 2), f"companyAuthStatus={r['data']['companyAuthStatus']}"

        # 3. 后台审核通过
        r = self.s.post(f"{ADMIN_URL}/admin-api/dist/team/apply-audit",
                        json={"id": apply_id, "status": 20},
                        headers=self.tu.admin_headers, verify=False).json()
        self.tu.assert_ok(r, "audit company team")

        # 4. DB 验证
        r = self.s.get(f"{APP_URL}/app-api/dist/promoter/info",
                       headers=self.tu.app_headers(token_a), verify=False).json()
        self.tu.assert_ok(r, "info after company team")
        team_id = r["data"]["teamInfo"]["teamId"]

        team_row = self.tu.db.fetch_one(
            "SELECT * FROM dist_team WHERE id=%s AND deleted=0", (team_id,))
        assert team_row["team_type"] == 2, f"teamType={team_row['team_type']} 应为2"
        assert team_row["company_auth_status"] is not None
        print(f"  企业团队: team_id={team_id}, team_type={team_row['team_type']}, "
              f"auth_status={team_row['company_auth_status']}")

    def test_company_team_commission(self):
        """企业团队正常分佣"""
        mobile_a = TeamUtils.gen_mobile()
        mobile_b = TeamUtils.gen_mobile()
        mobile_c = TeamUtils.gen_mobile()

        # 企业团队
        pid_a, token_a = self.tu.become_promoter(mobile_a)
        r = self.s.post(f"{APP_URL}/app-api/dist/team/apply", json={
            "teamType": 2, "teamName": f"co_{mobile_a[-4:]}",
            "mobile": mobile_a, "address": "地址",
            "socialAccount": "微信", "groupChannel": "微信社群",
        }, headers=self.tu.app_headers(token_a), verify=False).json()
        self.tu.assert_ok(r, "company team apply")
        apply_id = r["data"]["applyId"]
        self.s.post(f"{APP_URL}/app-api/dist/team/company-auth", json={
            "companyName": "测试企业有限公司", "creditCode": "91320594MA1M9K2Q3Y",
            "businessLicenseUrl": "https://example.com/l.jpg",
            "legalPersonName": "张三", "legalPersonIdCard": "110101199003071234",
            "legalIdCardFront": "", "legalIdCardBack": "",
            "businessScope": "回收", "businessValidDate": "2099-12-31",
        }, headers=self.tu.app_headers(token_a), verify=False)
        self.s.post(f"{ADMIN_URL}/admin-api/dist/team/apply-audit",
                    json={"id": apply_id, "status": 20},
                    headers=self.tu.admin_headers, verify=False)
        r = self.s.get(f"{APP_URL}/app-api/dist/promoter/info",
                       headers=self.tu.app_headers(token_a), verify=False).json()
        team_id = r["data"]["teamInfo"]["teamId"]

        # B 绑定 A 成为推广员 → 入团（需审核通过，全给团队下 B 的佣金才路由到团队）
        pid_b = self.tu.become_promoter(mobile_b, promoter_id=pid_a)[0]
        _, apply_id = self.tu.join_team(mobile_b, team_id)
        self.tu.audit_join(apply_id, token_a, status=20)

        # C 绑定 B → 下单
        token_c = self.tu.login.app_login_for_promoter(mobile=mobile_c, promoter_id=pid_b)
        before_b = self.tu.get_wallet_balance(pid_b, 1)
        before_t = self.tu.get_wallet_balance(team_id, 2)
        order_id = self.tu.settle_order(token_c, mobile_c)
        real_weight, total_price = self.tu.get_order_data(order_id)

        # 校验分佣（全给团队：B 个人无收益，团队全额入账）
        rules = self.tu.load_team_rules(token_a)
        info = self.tu.get_promoter_info(token_a)
        _, detail = self.tu.match_rule_detail(rules, info["level"], info["star"], real_weight)
        expected_personal, _, expected_team = self.tu.calc_team_split(detail, total_price)
        self.tu.assert_wallet_delta(team_id, 2, before_t,
                                    expected_personal + expected_team, label="企业团队")
        self.tu.assert_wallet_delta(pid_b, 1, before_b, 0, label="B个人")
