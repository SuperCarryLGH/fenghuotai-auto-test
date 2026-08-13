"""团队分销规则：校验 GET /app-api/dist/rule/get?promoteType=20 结构与非空字段"""
import pytest
from Common.team_utils import TeamUtils


class TestDistTeamRule:

    @pytest.fixture(autouse=True)
    def _setup(self, api_session, login_tool, admin_token, db_client):
        self.tu = TeamUtils(api_session, login_tool, db_client, admin_token)

    def _load_rules(self, token):
        rules = self.tu.load_team_rules(token)
        assert isinstance(rules, list), "team rules 不是 list"
        assert len(rules) > 0, "team rules 为空"
        return rules

    def _assert_rule_field_types(self, rule):
        assert isinstance(rule["ruleType"], int)
        assert isinstance(rule["level"], int)
        assert isinstance(rule["star"], int)
        assert isinstance(rule["maxFirstInviteNum"], int)
        assert rule["maxSecondInviteNum"] is None or isinstance(rule["maxSecondInviteNum"], int)
        assert isinstance(rule["upgradeOrderTarget"], int)

    def _assert_rule_detail_fields(self, detail):
        assert isinstance(detail["weightMin"], (int, float))
        assert isinstance(detail["weightMax"], (int, float))
        assert isinstance(detail["rewardMode"], int)
        assert isinstance(detail["firstFixedReward"], int)
        assert isinstance(detail["firstOrderRate"], (int, float))
        v1 = detail.get("firstOrderTeamRewardRate")
        v2 = detail.get("secondOrderTeamRewardRate")
        assert v1 is None or isinstance(v1, (int, float)), "firstOrderTeamRewardRate 类型异常"
        assert v2 is None or isinstance(v2, (int, float)), "secondOrderTeamRewardRate 类型异常"

    def test_team_rule_structure(self):
        """团队规则字段完整性"""
        mobile = TeamUtils.gen_mobile()
        _, token = self.tu.become_promoter(mobile)
        rules = self._load_rules(token)
        rule = rules[0]
        self._assert_rule_field_types(rule)
        assert rule["ruleType"] == 2, f"团队规则 ruleType={rule['ruleType']} 应为 2"
        details = rule.get("ruleDetails", [])
        assert len(details) > 0, "ruleDetails 为空"
        for detail in details:
            self._assert_rule_detail_fields(detail)

    def test_team_rule_vs_personal(self):
        """团队规则 vs 个人规则结构一致但 ruleType 不同"""
        mobile = TeamUtils.gen_mobile()
        _, token = self.tu.become_promoter(mobile)
        team_rules = self.tu.load_team_rules(token)
        personal_rules = self.tu.load_personal_rules(token)
        assert len(team_rules) > 0
        assert len(personal_rules) > 0
        assert team_rules[0]["ruleType"] == 2
        assert personal_rules[0]["ruleType"] == 1
