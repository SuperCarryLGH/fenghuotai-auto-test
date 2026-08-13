import pytest


class Test_AppApiRecycleClearOrderDriverDepart:
    """司机出发"""

    @pytest.mark.smoke
    def test_AppApiRecycleClearOrderDriverDepart(self, clear_chain):
        chain, co_id, driver_token, _ = clear_chain
        chain.driver_accept(co_id, driver_token)
        r = chain.driver_depart(co_id, driver_token)
        print(r)
