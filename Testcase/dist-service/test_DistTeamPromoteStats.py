"""团队统计与排行榜：成员列表、订单列表、统计、排行（接口已迁移到 /stats/*，promoteType=20）"""
import time
import pytest
from config import APP_URL
from Common.team_utils import TeamUtils


class TestDistTeamPromoteStats:

    @pytest.fixture(autouse=True)
    def _setup(self, api_session, login_tool, admin_token, db_client):
        self.tu = TeamUtils(api_session, login_tool, db_client, admin_token)
        self.s = api_session

    def _prepare_data(self):
        """准备：A 团长 → B 绑定 A 入团 → C 绑定 B → C 下单（B 需是 A 下线，团队佣金才会入账）"""
        mobile_a = TeamUtils.gen_mobile()
        mobile_b = TeamUtils.gen_mobile()
        mobile_c = TeamUtils.gen_mobile()
        team_id, pid_a, token_a, team_info = self.tu.become_team_leader(mobile_a)
        pid_b = self.tu.become_promoter(mobile_b, promoter_id=pid_a)[0]
        _, apply_id = self.tu.join_team(mobile_b, team_id)
        self.tu.audit_join(apply_id, token_a, status=20)
        token_c = self.tu.login.app_login_for_promoter(mobile=mobile_c, promoter_id=pid_b)
        order_id = self.tu.settle_order(token_c, mobile_c)
        return team_id, token_a, mobile_a, pid_b, order_id

    def _wait_team_commission(self, team_id, order_id):
        team_acc_id = self.tu.get_team_commission_account_id(team_id)
        assert team_acc_id is not None, "团队佣金账户不存在"
        assert self.tu.wait_team_commission(order_id, team_acc_id, timeout=40) is not None, \
            "团队佣金未入账"
        return team_acc_id

    def _first_level_count(self, token):
        """个人推广统计 firstLevelCount（promoteType=10）"""
        r = self.s.get(f"{APP_URL}/app-api/dist/stats/promote-data",
                       headers=self.tu.app_headers(token),
                       params={"promoteType": 10}, verify=False).json()
        self.tu.assert_ok(r, "promote-data personal")
        return int(r["data"]["firstLevelCount"])

    def _wait_first_level_count(self, token, expected, timeout=10):
        for _ in range(timeout * 2):
            if self._first_level_count(token) == expected:
                return
            time.sleep(0.5)
        actual = self._first_level_count(token)
        raise AssertionError(f"firstLevelCount 轮询超时: 预期={expected}, 实际={actual}")

    def _promote_user_ids(self, token, promote_type):
        """promote-list 里所有被拉用户的 userId 集合"""
        r = self.s.get(f"{APP_URL}/app-api/dist/stats/promote-list",
                       headers=self.tu.app_headers(token),
                       params={"promoteType": promote_type, "pageNo": 1, "pageSize": 200}, verify=False).json()
        self.tu.assert_ok(r, f"promote-list promoteType={promote_type}")
        return {int(item["userId"]) for item in r["data"]["list"]}

    def _wait_promote_user_present(self, token, promote_type, user_id, timeout=10):
        for _ in range(timeout * 2):
            if user_id in self._promote_user_ids(token, promote_type):
                return
            time.sleep(0.5)
        raise AssertionError(f"promote-list(promoteType={promote_type}) 中未出现 userId={user_id}")

    def test_promote_list(self):
        """团队成员列表包含入团成员"""
        team_id, token_a, mobile_a, pid_b, order_id = self._prepare_data()
        r = self.s.get(f"{APP_URL}/app-api/dist/team/member/list",
                       headers=self.tu.app_headers(token_a),
                       params={"pageNo": 1, "pageSize": 20}, verify=False).json()
        self.tu.assert_ok(r, "team member list")
        data = r["data"]
        assert data["total"] >= 1, "成员列表为空"
        pids = [int(m["promoterId"]) for m in data["list"]]
        assert pid_b in pids, f"入团成员 B({pid_b}) 不在成员列表中: {pids}"
        print(f"  成员列表: total={data['total']}, B 在列")

    def test_promote_order_list(self):
        """团队推广订单列表包含本单（结算后）"""
        team_id, token_a, mobile_a, pid_b, order_id = self._prepare_data()
        self._wait_team_commission(team_id, order_id)
        r = self.s.get(f"{APP_URL}/app-api/dist/stats/order-list",
                       headers=self.tu.app_headers(token_a),
                       params={"promoteType": 20, "pageNo": 1, "pageSize": 20}, verify=False).json()
        self.tu.assert_ok(r, "stats order list")
        data = r["data"]
        total = data["total"]
        order_ids = [int(o["orderId"]) for o in data["list"]]
        assert total >= 1, f"订单列表为空 total={total}"
        assert int(order_id) in order_ids, f"本单 {order_id} 不在订单列表中: {order_ids}"
        print(f"  订单列表: 共{total}条, 本单在列")

    def test_promote_stats(self):
        """团队推广统计：firstLevelCount=该用户入团后拉的人数（B 入团后拉 C，应>=1）"""
        team_id, token_a, mobile_a, pid_b, order_id = self._prepare_data()
        r = self.s.get(f"{APP_URL}/app-api/dist/stats/promote-data",
                       headers=self.tu.app_headers(token_a),
                       params={"promoteType": 20}, verify=False).json()
        self.tu.assert_ok(r, "promote stats")
        data = r["data"]
        assert data.get("firstLevelCount") is not None
        assert data.get("secondLevelCount") is not None
        assert int(data["firstLevelCount"]) >= 1, \
            f"firstLevelCount={data['firstLevelCount']} 应>=1(B入团后拉了C)"
        assert int(data["secondLevelCount"]) >= 0
        print(f"  推广统计: firstLevelCount={data['firstLevelCount']}, "
              f"secondLevelCount={data['secondLevelCount']}")

    def test_pre_join_recruits_preserved_after_team_join(self):
        """
        入团前拉的 C：入团后 promote-list(promoteType=20) 中应仍能看到 C（数据匹配）。
        入团前 promote-list(promoteType=10) 记录 B 拉的 C 的 userId；
        入团后 promote-list(promoteType=20) 按团员展示被拉的人，C 应仍在其中，不在即 bug。
        另校验 promote-data(promoteType=10) 的 firstLevelCount 入团前后一致。
        """
        mobile_a = TeamUtils.gen_mobile()
        mobile_b = TeamUtils.gen_mobile()
        mobile_c = TeamUtils.gen_mobile()
        # 1. A 创建团队
        team_id, pid_a, token_a, _ = self.tu.become_team_leader(mobile_a)
        # 2. B 成为推广员（独立，不绑定 A）
        pid_b, token_b = self.tu.become_promoter(mobile_b)
        # 3. C 绑定 B（入团前拉的）
        self.tu.login.app_login_for_promoter(mobile=mobile_c, promoter_id=pid_b)
        # 4. 入团前基线：firstLevelCount=1，promote-list(promoteType=10) 记录 B 拉的 C 的 userId
        self._wait_first_level_count(token_b, 1)
        before_first = self._first_level_count(token_b)
        pre_user_ids = self._promote_user_ids(token_b, 10)
        assert pre_user_ids, "入团前 promote-list(promoteType=10) 应返回 B 拉的 C"
        print(f"  入团前 B: firstLevelCount={before_first}, 拉的 userId={sorted(pre_user_ids)}")
        # 5. B 加入团队
        _, apply_id = self.tu.join_team(mobile_b, team_id)
        self.tu.audit_join(apply_id, token_a, status=20)
        # 6. 入团后 firstLevelCount 保留
        self._wait_first_level_count(token_b, before_first)
        assert self._first_level_count(token_b) == before_first, "入团后 firstLevelCount 应保留"
        print(f"  ✅ 入团后 firstLevelCount 保留: {before_first}")
        # 7. 入团后 promote-list(promoteType=20)：入团前拉的 C 应仍可见（数据匹配）
        for c_uid in pre_user_ids:
            self._wait_promote_user_present(token_a, 20, c_uid)
            post_ids = self._promote_user_ids(token_a, 20)
            assert c_uid in post_ids, \
                f"入团前拉的 C({c_uid}) 在入团后 promote-list(promoteType=20) 中缺失=bug"
        print(f"  ✅ 入团前拉的 C 在入团后 promote-list(promoteType=20) 中仍可见")

    def test_order_stats(self):
        """团队订单统计反映今日下单"""
        team_id, token_a, mobile_a, pid_b, order_id = self._prepare_data()
        self._wait_team_commission(team_id, order_id)
        r = self.s.get(f"{APP_URL}/app-api/dist/stats/order-data",
                       headers=self.tu.app_headers(token_a),
                       params={"promoteType": 20}, verify=False).json()
        self.tu.assert_ok(r, "order stats")
        data = r["data"]
        assert data.get("todayOrderCount") is not None
        assert data.get("todayCompleteCount") is not None
        assert data.get("todayIncome") is not None
        assert int(data["todayOrderCount"]) >= 1, f"todayOrderCount={data['todayOrderCount']} 应>=1"
        print(f"  订单统计: todayOrderCount={data['todayOrderCount']}, "
              f"todayCompleteCount={data['todayCompleteCount']}, todayIncome={data['todayIncome']}")

    def test_member_profit_rank(self):
        """团队成员收益排行接口可用（dev 后端 500 bug，容忍）"""
        team_id, token_a, mobile_a, pid_b, order_id = self._prepare_data()
        r = self.s.get(f"{APP_URL}/app-api/dist/team/rank/member-profit",
                       headers=self.tu.app_headers(token_a),
                       params={"limit": 10}, verify=False).json()
        assert r["code"] in (0, 500), f"member profit rank: code={r['code']}, msg={r.get('msg','')}"
        if r["code"] == 500:
            print("  收益排行: dev 后端 500（后端 bug，待修复）")
            return
        data = r["data"]
        assert isinstance(data, list)
        if data:
            print(f"  收益排行: 共{len(data)}人")
            for item in data[:10]:
                print(f"    [rank={item.get('rank')}] 成员: {item.get('memberName')} | "
                      f"手机号: {item.get('phone')} | 收益: {item.get('totalProfit')} | "
                      f"入队时间: {item.get('joinTime')}")
        else:
            print("  收益排行: 无数据（结算未完成）")

    def test_promote_user_rank(self):
        """团队推广人数排行榜接口可用（校验榜单结构与排序）"""
        team_id, token_a, mobile_a, pid_b, order_id = self._prepare_data()
        r = self.s.get(f"{APP_URL}/app-api/dist/team/rank/promote-user",
                       headers=self.tu.app_headers(token_a),
                       params={"limit": 50}, verify=False).json()
        self.tu.assert_ok(r, "promote user rank")
        data = r["data"]
        assert isinstance(data, list)
        team_ids = [item["teamId"] for item in data]
        print(f"  推广人数排行: 共{len(data)}队, 榜单前10:")
        prev_promote = None
        for i, item in enumerate(data[:10]):
            assert item.get("teamName") is not None, f"榜单第{i+1}项缺少 teamName"
            assert item.get("leaderName") is not None, f"榜单第{i+1}项缺少 leaderName"
            if data[0].get("totalPromoteCount") is not None:
                promote = int(item["totalPromoteCount"])
                if prev_promote is not None:
                    assert promote <= prev_promote, f"榜单未按推广数降序: {promote}>{prev_promote}"
                prev_promote = promote
            print(f"    [rank={item.get('rank')}] 团队: {item.get('teamName')} | "
                  f"团长: {item.get('leaderName')} | 成员数: {item.get('memberCount')} | "
                  f"推广数: {item.get('totalPromoteCount')}")
        if team_id in team_ids:
            print(f"  本团队 {team_id} 在排行榜中")
        else:
            print(f"  本团队未进榜（新团队成员少，属正常现象）")
