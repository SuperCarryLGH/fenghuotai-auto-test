import pytest
from config import APP_URL
from Common.login import Login


class TestRecycleExpressOrderstatepushSf:

    @pytest.mark.smoke
    def test_TestRecycleExpressOrderstatepushSf(self,api_session,login_tool):
        mobile = "18338956022"
        token = login_tool.app_login(mobile=mobile)
        headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}

        url = f"{APP_URL}/app-api/recycle/express/order-state-push/sf"
        payload = {
                  "requestId": "",
                  "timestamp": "",
                  "orderState": [
                    {
                      "orderNo": "",
                      "waybillNo": "",
                      "orderStateCode": "",
                      "orderStateDesc": "",
                      "empCode": "",
                      "empPhone": "",
                      "netCode": "",
                      "lastTime": "",
                      "bookTime": "",
                      "carrierCode": "",
                      "createTm": ""
                }
              ]
            }

        resp = api_session.post(url, json=payload, headers=headers)
        assert resp.status_code == 200
        data = resp.json()
        assert data["code"] == 0
        print(data)
