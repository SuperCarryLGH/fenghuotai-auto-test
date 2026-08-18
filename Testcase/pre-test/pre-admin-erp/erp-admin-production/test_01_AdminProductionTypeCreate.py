import pytest


class TestAdminProductionTypeCreate:
    """创建生产类型"""

    @pytest.mark.smoke
    def test_admin_production_type_create(self, production_type_create):
        production_type_id = production_type_create
        assert production_type_id, "生产类型创建失败，返回 id 为空"
        print(f"生产类型创建成功，id：{production_type_id}")
