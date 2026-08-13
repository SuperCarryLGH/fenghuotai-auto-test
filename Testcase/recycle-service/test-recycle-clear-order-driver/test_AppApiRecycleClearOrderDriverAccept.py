import pytest


class Test_AppApiRecycleClearOrderDriverAccept:
    """司机接单"""

    @pytest.mark.smoke
    def test_AppApiRecycleClearOrderDriverAccept(self, clear_chain):
        chain, co_id, driver_token, _ = clear_chain
        r = chain.driver_accept(co_id, driver_token)
        print(r)
