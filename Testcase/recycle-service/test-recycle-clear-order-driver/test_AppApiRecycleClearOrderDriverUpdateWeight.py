import pytest


class Test_AppApiRecycleClearOrderDriverUpdateWeight:
    """司机更新重量"""

    @pytest.mark.smoke
    def test_AppApiRecycleClearOrderDriverUpdateWeight(self, clear_chain):
        chain, co_id, driver_token, _ = clear_chain
        chain.driver_accept(co_id, driver_token)
        chain.driver_depart(co_id, driver_token)
        chain.driver_arrive(co_id, driver_token)
        r = chain.driver_weigh(co_id, driver_token)
        print(r)
