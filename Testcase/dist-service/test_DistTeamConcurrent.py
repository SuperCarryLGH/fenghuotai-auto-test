"""并发测试：并发入团 + 并发下单分佣"""
import pytest
from concurrent.futures import ThreadPoolExecutor
from config import APP_URL
from Common.team_utils import TeamUtils


class TestDistTeamConcurrent:

    @pytest.fixture(autouse=True)
    def _setup(self, api_session, login_tool, admin_token, db_client):
        self.tu = TeamUtils(api_session, login_tool, db_client, admin_token)
        self.s = api_session

    def test_concurrent_join(self):
        """5 个推广官并发申请入团→团长批量审核"""
        mobile_a = TeamUtils.gen_mobile()
        team_id, _, token_a, _ = self.tu.become_team_leader(mobile_a)
        N = 5
        mobiles = [TeamUtils.gen_mobile() for _ in range(N)]
        for mb in mobiles:
            self.tu.become_promoter(mb)

        def _apply(i):
            t = self.tu.login.app_login_for_promoter(mobile=mobiles[i])
            r = self.s.post(f"{APP_URL}/app-api/dist/team/join",
                            json={"teamId": team_id},
                            headers=self.tu.app_headers(t),
                            verify=False).json()
            self.tu.assert_ok(r, f"{mobiles[i]} join")
            return r["data"]["applyId"]

        with ThreadPoolExecutor(max_workers=5) as pool:
            apply_ids = list(pool.map(_apply, range(N)))
        print(f"  并发入团申请: {len(apply_ids)} 个")

        for aid in apply_ids:
            self.tu.audit_join(aid, token_a, status=20)

        cnt = self.tu.db.fetch_one(
            "SELECT COUNT(*) as cnt FROM dist_team_promoter_relation "
            "WHERE team_id=%s AND status=20 AND team_user_type=20 AND deleted=0", (team_id,))
        assert cnt["cnt"] >= N, f"通过团员={cnt['cnt']}, 预期>={N}"
        print(f"  ✅ 团员入团 {cnt['cnt']} 个 (预期{N})")

    def test_concurrent_orders_settle(self):
        """5 个团员各自下线并发下单（流程校验，dev 不结算佣金）"""
        mobile_a = TeamUtils.gen_mobile()
        N = 3

        team_id, _, token_a, _ = self.tu.become_team_leader(mobile_a)

        member_pids = []
        for i in range(N):
            mb = TeamUtils.gen_mobile()
            self.tu.become_promoter(mb)
            _, apply_id = self.tu.join_team(mb, team_id)
            self.tu.audit_join(apply_id, token_a, status=20)
            pid = self.tu.get_promoter_id_by_mobile(mb)
            member_pids.append(pid)

        def _place(i):
            pid = member_pids[i]
            mc = TeamUtils.gen_mobile()
            self.tu.become_promoter(mc, promoter_id=pid)
            t = self.tu.login.app_login_for_promoter(mobile=mc, promoter_id=pid)
            order_id = self.tu.settle_order(t, mc)
            return order_id

        with ThreadPoolExecutor(max_workers=3) as pool:
            order_ids = list(pool.map(_place, range(N)))
        print(f"  并发下单: {len(order_ids)} 笔 (流程完成)")
        # dev 不结算佣金，仅验证并发流程无报错
        print(f"  ✅ 并发 {N} 笔下单流程通过")
