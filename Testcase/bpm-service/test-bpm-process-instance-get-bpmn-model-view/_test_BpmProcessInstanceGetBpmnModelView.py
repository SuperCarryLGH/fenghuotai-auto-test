import pytest
from config import ADMIN_URL


class TestBpmProcessInstanceGetBpmnModelView:
    """获取流程实例的 BPMN 模型视图"""

    @pytest.mark.smoke
    def test_BpmProcessInstanceGetBpmnModelView(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/bpm/process-instance/get-bpmn-model-view"
        params = {
            # TODO: 补充查询参数
        }
        resp = api_session.get(url, params=params, headers=auth_headers)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)

 == 200
        r = resp.json()
        assert r["code"] == 0
        print(r)
