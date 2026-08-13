"""团队解散：团长退出导致团队关闭（走 admin DELETE）"""
import pytest
from config import ADMIN_URL
from Common.team_utils import TeamUtils


class TestDistTeamDisband:

    @pytest.fixture(autouse=True)
    def _setup(self, api_session, login_tool, admin_token, db_client):
        self.tu = TeamUtils(api_session, login_tool, db_client, admin_token)
        self.s = api_session

    def test_leader_quit_no_member(self):
        """团长删除团队（无团员）"""
        mobile_a = TeamUtils.gen_mobile()
        team_id, _, token_a, _ = self.tu.become_team_leader(mobile_a)
        r = self.s.delete(f"{ADMIN_URL}/admin-api/dist/team/delete",
                          headers=self.tu.admin_headers,
                          params={"id": team_id}, verify=False).json()
        self.tu.assert_ok(r, "leader delete team")
        # DB 团队被软删除
        row = self.tu.db.fetch_one(
            "SELECT deleted FROM dist_team WHERE id=%s", (team_id,))
        assert row["deleted"] == b'\x01', f"团队 deleted={row['deleted']} 应为1(已删除)"
        print(f"  ✅ 团队已软删除 team_id={team_id}")

    def test_leader_quit_with_members(self):
        """团长删除团队（有团员时）"""
        mobile_a = TeamUtils.gen_mobile()
        mobile_b = TeamUtils.gen_mobile()
        team_id, _, token_a, _ = self.tu.become_team_leader(mobile_a)
        # 先有团员
        _, apply_id = self.tu.join_team(mobile_b, team_id)
        self.tu.audit_join(apply_id, token_a, status=20)
        r = self.s.delete(f"{ADMIN_URL}/admin-api/dist/team/delete",
                          headers=self.tu.admin_headers,
                          params={"id": team_id}, verify=False).json()
        self.tu.assert_ok(r, "leader delete team with members")
        row = self.tu.db.fetch_one(
            "SELECT deleted FROM dist_team WHERE id=%s", (team_id,))
        assert row["deleted"] == b'\x01', f"团队 deleted={row['deleted']} 应为1"
        print(f"  ✅ 团队已软删除 team_id={team_id}（含团员）")
