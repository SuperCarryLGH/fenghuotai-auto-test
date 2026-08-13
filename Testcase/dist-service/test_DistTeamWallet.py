"""团队钱包：钱包查询、流水（接口已迁移到 /dist/wallet/*，promoteType=20；提现已跳过）"""
import datetime
import pytest
from config import APP_URL, ADMIN_URL
from Common.team_utils import TeamUtils


class TestDistTeamWallet:

    @pytest.fixture(autouse=True)
    def _setup(self, api_session, login_tool, admin_token, db_client):
        self.tu = TeamUtils(api_session, login_tool, db_client, admin_token)
        self.s = api_session

    def _prepare_commission(self):
        """准备：A 团长 → B 绑定 A 入团 → C 下单 → A 团队二级佣金入账"""
        mobile_a = TeamUtils.gen_mobile()
        mobile_b = TeamUtils.gen_mobile()
        mobile_c = TeamUtils.gen_mobile()
        team_id, pid_a, token_a, team_info = self.tu.become_team_leader(mobile_a)
        pid_b = self.tu.become_promoter(mobile_b, promoter_id=pid_a)[0]
        self.tu.join_team(mobile_b, team_id)
        token_c = self.tu.login.app_login_for_promoter(mobile=mobile_c, promoter_id=pid_b)
        order_id = self.tu.settle_order(token_c, mobile_c)
        team_acc_id = self.tu.get_team_commission_account_id(team_id)
        actual = self.tu.wait_team_commission(order_id, team_acc_id, timeout=30)
        assert actual is not None, "团队佣金未入账，无法继续钱包测试"
        return team_id, token_a, team_acc_id

    def _wallet(self, token_a):
        return self.s.get(f"{APP_URL}/app-api/dist/wallet/wallet",
                          headers=self.tu.app_headers(token_a),
                          params={"promoteType": 20}, verify=False).json()

    def test_team_wallet_balance(self):
        """团队钱包余额 > 0"""
        team_id, token_a, acc_id = self._prepare_commission()
        r = self._wallet(token_a)
        self.tu.assert_ok(r, "team wallet")
        data = r["data"]
        assert int(data["accountId"]) == acc_id
        assert int(data["balance"]) > 0, f"钱包余额={data['balance']} 应>0"
        assert int(data["totalIncome"]) > 0
        print(f"  团队钱包: balance={data['balance']}, totalIncome={data['totalIncome']}")

    def test_team_wallet_records(self):
        """团队钱包流水有入账记录"""
        team_id, token_a, acc_id = self._prepare_commission()
        today = datetime.date.today().strftime("%Y-%m-%d")
        r = self.s.get(f"{APP_URL}/app-api/dist/wallet/wallet/records",
                       headers=self.tu.app_headers(token_a),
                       params={"startDate": today, "endDate": today,
                               "pageNo": 1, "pageSize": 20, "promoteType": 20}, verify=False).json()
        self.tu.assert_ok(r, "wallet records")
        total = r["data"]["total"]
        assert total >= 1, f"钱包流水为空 total={total}"
        records = r["data"]["list"]
        if records:
            rec = records[0]
            assert int(rec.get("price", 0)) > 0
            assert rec.get("sourceType") in (10, 20, 21), f"sourceType={rec.get('sourceType')}"
            assert rec.get("status") == 1, f"status={rec.get('status')} 应为1(已入账)"
        print(f"  钱包流水: 共{total}条")

    @pytest.mark.skip(reason="随机账号无法登录核销；dev 配置提现渠道后会真实提现造成资金损失，暂不执行")
    def test_withdraw_apply(self):
        """团队提现申请（已跳过：避免随机账号真实提现）"""
        team_id, token_a, acc_id = self._prepare_commission()
        r = self._wallet(token_a)
        balance = int(r["data"]["balance"])
        if balance <= 0:
            print("  ⚠ 余额不足，跳过提现测试")
            return
        withdraw_amount = min(balance, 100)  # 提至少 1 元（单位分）
        r = self.s.post(f"{APP_URL}/app-api/dist/wallet/withdraw",
                        json={"amount": withdraw_amount, "platform": "WECHAT_MP", "promoteType": 20},
                        headers=self.tu.app_headers(token_a), verify=False).json()
        if r["code"] == 10030:
            print("  ⚠ 提现平台不支持(dev 未配置渠道，后端行为)，跳过提现流程")
            return
        self.tu.assert_ok(r, "withdraw apply")
        withdraw_id = r["data"]
        print(f"  提现申请: id={withdraw_id}, amount={withdraw_amount}")

        # 后台审核通过
        r = self.s.put(f"{ADMIN_URL}/admin-api/dist/commission-withdraw/audit",
                        json={"id": withdraw_id, "approve": True, "remark": "test"},
                        headers=self.tu.admin_headers, verify=False).json()
        self.tu.assert_ok(r, "withdraw audit")
        print(f"  提现审核通过")

        # 余额扣减
        import time
        time.sleep(1)
        r = self._wallet(token_a)
        new_balance = int(r["data"]["balance"])
        assert new_balance < balance or new_balance == balance - withdraw_amount, \
            f"提现后余额={new_balance}, 原余额={balance}, 提现额={withdraw_amount}"
        print(f"  提现后余额: {new_balance} (原 {balance} - {withdraw_amount})")
