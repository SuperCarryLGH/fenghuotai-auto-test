import pytest


class Test_AppApiRecycleClearOrderDriverCancel:
    """司机取消"""

    @pytest.mark.smoke
    def test_AppApiRecycleClearOrderDriverCancel(self, clear_chain):
        chain, co_id, driver_token, _ = clear_chain
        chain.driver_accept(co_id, driver_token)
        r = chain.driver_cancel(co_id, driver_token)
        print(r)
