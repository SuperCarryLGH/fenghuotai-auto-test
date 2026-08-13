import pytest


class Test_AppApiRecycleClearOrderDriverGet:
    """司机获取详情"""

    @pytest.mark.smoke
    def test_AppApiRecycleClearOrderDriverGet(self, clear_chain):
        chain, co_id, driver_token, _ = clear_chain
        r = chain.driver_get(co_id, driver_token)
        print(r)
