"""团队申请：校验申请→审核→团队创建→DB 全流程"""
import pytest
from config import APP_URL
from Common.team_utils import TeamUtils


class TestDistTeamApply:

    @pytest.fixture(autouse=True)
    def _setup(self, api_session, login_tool, admin_token, db_client):
        self.tu = TeamUtils(api_session, login_tool, db_client, admin_token)
        self.s = api_session

    def test_apply_audit_team(self):
        """申请团队→审核通过→DB 确认"""
        mobile_a = TeamUtils.gen_mobile()
        team_id, pid_a, token_a, team_info = self.tu.become_team_leader(mobile_a)
        # 1.0 promoter/info 的 teamInfo 字段完整
        assert int(team_info["teamId"]) == team_id
        assert team_info.get("teamName") is not None
        assert int(team_info["leaderPromoterId"]) == pid_a
        assert team_info.get("teamLevel") is not None
        assert team_info.get("teamStar") is not None
        # 1.1 DB 团队主表存在
        team_row = self.tu.db.fetch_one(
            "SELECT * FROM dist_team WHERE id=%s AND deleted=0", (team_id,))
        assert team_row, f"dist_team id={team_id} 不存在"
        assert team_row["leader_promoter_id"] == pid_a
        assert team_row["team_type"] == 1
        assert team_row["status"] == 20
        # 1.2 DB 团长关系存在
        rel_row = self.tu.db.fetch_one(
            "SELECT * FROM dist_team_promoter_relation WHERE team_id=%s AND promoter_id=%s AND deleted=0",
            (team_id, pid_a))
        assert rel_row, f"团长关系不存在 team_id={team_id} promoter_id={pid_a}"
        assert rel_row["team_user_type"] == 10, f"teamUserType={rel_row['team_user_type']} 应为10"
        assert rel_row["status"] == 20, f"status={rel_row['status']} 应为20"
        assert rel_row["join_type"] == 10, f"joinType={rel_row['join_type']} 应为10"
        # 1.3 DB 团队佣金账户自动创建
        acc_id = self.tu.get_team_commission_account_id(team_id)
        assert acc_id is not None, f"团队佣金账户未创建 team_id={team_id}"
        # 1.4 团队名称
        assert team_row["team_name"] is not None

    def test_team_info_app(self):
        """APP 推广官资料可查到自己的团队"""
        mobile_a = TeamUtils.gen_mobile()
        team_id, pid_a, token_a, _ = self.tu.become_team_leader(mobile_a)
        team_info = self.tu.get_promoter_info(token_a)["teamInfo"]
        assert int(team_info["teamId"]) == team_id, f"teamId={team_info['teamId']} 应={team_id}"
        assert int(team_info["leaderPromoterId"]) == pid_a
        print(f"  APP 团队信息: teamId={team_id}, leaderPromoterId={pid_a}")

    def test_duplicate_team_apply(self):
        """同一推广官重复申请应返回业务错误"""
        mobile_a = TeamUtils.gen_mobile()
        _, _, token_a, _ = self.tu.become_team_leader(mobile_a)
        r = self.s.post(f"{APP_URL}/app-api/dist/team/apply", json={
            "teamType": 1, "teamName": "dup",
            "mobile": mobile_a, "address": "测试",
            "socialAccount": "微信", "groupChannel": "微信社群",
        }, headers=self.tu.app_headers(token_a), verify=False).json()
        assert r["code"] == 10013, f"重复申请应返回10013(推广团队申请已存在), 实际 code={r['code']}, msg={r.get('msg','')}"
        print(f"  重复申请团队 → code=10013, 已拦截")
