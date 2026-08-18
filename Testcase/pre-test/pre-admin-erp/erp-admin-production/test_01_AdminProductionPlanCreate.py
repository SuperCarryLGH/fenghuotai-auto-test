import pytest


class TestAdminProductionPlanCreate:
    """创建生产计划"""

    @pytest.mark.smoke
    def test_admin_production_plan_create(self, production_plan_create):
        production_id = production_plan_create
        print(f"生产计划创建成功：", production_id)