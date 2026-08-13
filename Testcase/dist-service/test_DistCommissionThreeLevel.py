"""三级分佣校验：A→B→C→D→D下单，C一级 B二级 A三级无佣金"""
import time
import pytest
from config import APP_URL
from Common.team_utils import TeamUtils


class TestDistCommissionThreeLevel:

    @pytest.fixture(autouse=True)
    def _setup(self, api_session, login_tool, admin_token, db_client):
        self.tu = TeamUtils(api_session, login_tool, db_client, admin_token)

    def test_three_level_no_commission(self):
        """A→B→C→D，D 下单 C 一级 B 二级 A 三级无佣金"""
        suffix = str(int(time.time() * 1000))[-8:]
        mobile_a = "156" + suffix
        mobile_b = "156" + str(int(suffix) + 1).zfill(8)
        mobile_c = "156" + str(int(suffix) + 2).zfill(8)
        mobile_d = "156" + str(int(suffix) + 3).zfill(8)

        pid_a, token_a = self.tu.become_promoter(mobile_a)

        pid_b, token_b = self.tu.become_promoter(mobile_b, promoter_id=pid_a)

        token_c = self.tu.login.app_login_for_promoter(mobile=mobile_c,
                                                       promoter_id=pid_b)
        pid_c, _ = self.tu.become_promoter(mobile_c)

        token_d = self.tu.login.app_login_for_promoter(mobile=mobile_d,
                                                       promoter_id=pid_c)

        oid_b = self.tu.settle_order(token_b, mobile_b)
        assert self.tu.wait_personal_commission(oid_b, pid_a, timeout=15) > 0

        oid_c = self.tu.settle_order(token_c, mobile_c)
        assert self.tu.wait_personal_commission(oid_c, pid_b, timeout=15) > 0
        assert self.tu.wait_personal_commission(oid_c, pid_a, timeout=15) > 0

        bal_before = self.tu.get_promoter_info(token_a)["commissionBalance"]

        oid_d = self.tu.settle_order(token_d, mobile_d)
        time.sleep(3)
        bal_after = self.tu.get_promoter_info(token_a)["commissionBalance"]
        assert bal_after == bal_before, f"A 应有余额变化: {bal_before}→{bal_after}"
        print(f"  ✅ A 三级无佣金 (余额={bal_after})")
