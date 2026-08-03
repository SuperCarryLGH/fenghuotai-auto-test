"""入团申请+审核：校验申请→团长审核→DB 状态"""
import pytest
from config import APP_URL
from Common.team_utils import TeamUtils


class TestDistTeamJoinAudit:

    @pytest.fixture(autouse=True)
    def _setup(self, api_session, login_tool, admin_token, db_client):
        self.tu = TeamUtils(api_session, login_tool, db_client, admin_token)
        self.s = api_session

    def _print_team(self, mobile_a, team_id):
        row = self.tu.db.fetch_one(
            "SELECT team_name FROM dist_team WHERE id=%s AND deleted=0", (team_id,))
        print(f"  团长 {mobile_a} 创建团队 team_id={team_id}"
              + (f", 团队名={row['team_name']}" if row else ""))

    def test_leader_audit_pass(self):
        """团长审核通过→DB 状态变为已加入（含入团申请）"""
        mobile_a = TeamUtils.gen_mobile()
        mobile_b = TeamUtils.gen_mobile()
        team_id, _, token_a, _ = self.tu.become_team_leader(mobile_a)
        self._print_team(mobile_a, team_id)
        token_b, apply_id = self.tu.join_team(mobile_b, team_id)
        print(f"  团员 {mobile_b} 申请入团 apply_id={apply_id}")
        self.tu.audit_join(apply_id, token_a, status=20)
        print(f"  团长审核通过 → 成员正式入团")
        pid_b = self.tu.get_promoter_id_by_mobile(mobile_b)
        row = self.tu.db.fetch_one(
            "SELECT * FROM dist_team_promoter_relation WHERE team_id=%s AND promoter_id=%s AND deleted=0",
            (team_id, pid_b))
        assert row["status"] == 20, f"审核后 status={row['status']} 应为20"
        assert row["join_time"] is not None, "join_time 应为非空"
        assert row["settle_status"] == 10, f"settleStatus={row['settle_status']} 应为10(参与分佣)"
        print(f"  DB 关系: promoterId={pid_b}, status=20(已加入), "
              f"join_time={row['join_time']}, settle_status=10(参与分佣)")
        print(f"  ✅ 审核通过后成员状态正确")

    def test_leader_audit_reject(self):
        """团长拒绝入团 → 不应产生成员关系（后端 bug：仍写 status=20，预期失败）"""
        mobile_a = TeamUtils.gen_mobile()
        mobile_b = TeamUtils.gen_mobile()
        team_id, _, token_a, _ = self.tu.become_team_leader(mobile_a)
        self._print_team(mobile_a, team_id)
        token_b, apply_id = self.tu.join_team(mobile_b, team_id)
        print(f"  团员 {mobile_b} 申请入团 apply_id={apply_id}")
        self.tu.audit_join(apply_id, token_a, status=30, remark="测试拒绝")
        print(f"  团长拒绝入团 (备注=测试拒绝)") 
        pid_b = self.tu.get_promoter_id_by_mobile(mobile_b)
        row = self.tu.db.fetch_one(
            "SELECT * FROM dist_team_promoter_relation WHERE team_id=%s AND promoter_id=%s AND deleted=0",
            (team_id, pid_b))
        assert row is None or row["status"] != 20, \
            f"拒绝后仍存在生效成员关系 status={row['status'] if row else None}，应为无"
        print(f"  ✅ 拒绝后无成员关系")

    def test_duplicate_join(self):
        """已加入后再次申请应失败"""
        mobile_a = TeamUtils.gen_mobile()
        mobile_b = TeamUtils.gen_mobile()
        team_id, _, token_a, _ = self.tu.become_team_leader(mobile_a)
        self._print_team(mobile_a, team_id)
        _, apply_id = self.tu.join_team(mobile_b, team_id)
        self.tu.audit_join(apply_id, token_a, status=20)
        print(f"  团员 {mobile_b} 已入团成功")
        # 再次申请
        token_b2 = self.tu.login.app_login_for_promoter(mobile=mobile_b)
        r = self.s.post(f"{APP_URL}/app-api/dist/team/join", json={"teamId": team_id},
                        headers=self.tu.app_headers(token_b2), verify=False).json()
        assert r["code"] == 10021, f"重复入团应返回10021(用户关系已存在), 实际 code={r['code']}, msg={r.get('msg','')}"
        print(f"  团员再次申请入团 → code={r['code']}, msg={r.get('msg','')}")
        print(f"  ✅ 重复入团被拦截")

    def test_member_list(self):
        """APP 团队成员列表可查到新入团成员"""
        mobile_a = TeamUtils.gen_mobile()
        mobile_b = TeamUtils.gen_mobile()
        team_id, _, token_a, _ = self.tu.become_team_leader(mobile_a)
        self._print_team(mobile_a, team_id)
        _, apply_id = self.tu.join_team(mobile_b, team_id)
        pid_b = self.tu.get_promoter_id_by_mobile(mobile_b)
        self.tu.audit_join(apply_id, token_a, status=20)
        r = self.s.get(f"{APP_URL}/app-api/dist/team/member/list",
                       headers=self.tu.app_headers(token_a),
                       params={"pageNo": 1, "pageSize": 20}, verify=False).json()
        self.tu.assert_ok(r, "member list")
        pids = [int(item["promoterId"]) for item in r["data"]["list"]]
        assert pid_b in pids, f"成员 pid={pid_b} 未在成员列表中"
        print(f"  APP 成员列表: total={r['data']['total']}")
        print(f"  成员 promoterId: {pids}")
        print(f"  ✅ 新入团成员 {pid_b} 在成员列表中")

    def test_audit_list(self):
        """团长待审核列表展示申请"""
        mobile_a = TeamUtils.gen_mobile()
        mobile_b = TeamUtils.gen_mobile()
        team_id, _, token_a, _ = self.tu.become_team_leader(mobile_a)
        self._print_team(mobile_a, team_id)
        _, apply_id = self.tu.join_team(mobile_b, team_id)
        r = self.s.get(f"{APP_URL}/app-api/dist/team/audit-list",
                       headers=self.tu.app_headers(token_a),
                       params={"pageNo": 1, "pageSize": 20}, verify=False).json()
        self.tu.assert_ok(r, "audit list")
        ids = [item["applyId"] for item in r["data"]["list"]] #获取的数据
        assert apply_id in ids, f"申请 apply_id={apply_id} 未在待审核列表中"
        print(f"  团长 {mobile_a} 查询待审核列表 → total={r['data']['total']}")
        print(f"  ✅ 申请 apply_id={apply_id} 在待审核列表中")
