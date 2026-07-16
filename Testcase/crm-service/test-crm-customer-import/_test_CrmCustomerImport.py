import pytest
from config import ADMIN_URL


class TestCrmCustomerImport:
    """导入客户"""

    @pytest.mark.smoke
    def test_CrmCustomerImport(self, api_session, auth_headers):
        url = f"{ADMIN_URL}/admin-api/crm/customer/import"
        # 导入接口，需构造 multipart/form-data + 文件
                body = {
            # TODO: 补充创建参数
        }
        resp = api_session.post(url, json=body, headers=auth_headers)
