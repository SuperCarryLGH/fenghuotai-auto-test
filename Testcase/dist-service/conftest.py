"""推广达人测试 fixtures"""
import time
import pytest
from config import APP_URL, ADMIN_URL
from Common.login import Login

ID_CARD = "https://gips2.baidu.com/it/u=195724436,3554684702&fm=3028&app=3028&f=JPEG&fmt=auto?w=1280&h=960"


@pytest.fixture(scope="session")
def promoter_headers(login_tool):
    """推广申请/排行/钱包"""
    token = login_tool.app_login(mobile="15606103874")
    return {
        **Login.SMS_LOGIN_HEADERS,
        "timestamp": str(int(time.time() * 1000)),
        "Authorization": f"Bearer {token}",
    }


@pytest.fixture(scope="session")
def promoterinfo_headers(login_tool):
    """推广信息/实名/签约"""
    token = login_tool.app_login(mobile="15610173675")
    return {
        **Login.SMS_LOGIN_HEADERS,
        "timestamp": str(int(time.time() * 1000)),
        "Authorization": f"Bearer {token}",
    }


@pytest.fixture(scope="session")
def rulepersonal_headers(login_tool):
    """分销规则"""
    token = login_tool.app_login(mobile="15610173675")
    return {
        **Login.SMS_LOGIN_HEADERS,
        "timestamp": str(int(time.time() * 1000)),
        "Authorization": f"Bearer {token}",
    }


def _new_mobile():
    """生成不重复手机号"""
    return "159" + str(int(time.time() * 1000))[-8:]


@pytest.fixture(scope="session")
def autotest_promoter_headers(api_session, login_tool, admin_token):
    """动态注册并认证一个推广员，返回带鉴权 headers（该推广员已实名+签约）"""
    mobile = _new_mobile()
    token = login_tool.app_login(mobile=mobile)

    def app_headers(t):
        return {**Login.SMS_LOGIN_HEADERS, "timestamp": str(int(time.time() * 1000)),
                "Authorization": f"Bearer {t}"}

    def app_get(url, t):
        return api_session.get(url, headers=app_headers(t), verify=False).json()

    def app_post(url, body, t):
        return api_session.post(url, json=body, headers=app_headers(t), verify=False).json()

    admin_headers = {**Login.ADMIN_LOGIN_HEADERS, "Authorization": f"Bearer {admin_token}"}
    hs = app_headers(token)

    # 1. 申请推广官
    body = {
        "mobile": mobile, "provinceCode": "", "provinceName": "江苏省",
        "cityCode": "", "cityName": "苏州市", "districtCode": "", "districtName": "姑苏区",
        "promoteMode": 1, "hasMediaAccount": 1, "mediaAccountType": "",
        "mediaOtherDesc": "", "hasOfflineResource": 0, "offlineResource": "",
        "resourceOtherDesc": "", "hasSimilarExp": 1, "similarExp": "", "expOtherDesc": "",
        "mediaScreenshot": "",
    }
    r = app_post(f"{APP_URL}/app-api/dist/promoter/apply", body, token)
    assert r["code"] in (0, "0", 100, "100"), f"申请推广官失败: {r}"
    apply_id = r["data"]["applyId"] if isinstance(r["data"], dict) else None
    if apply_id is None:
        # 已申请过则查询补录 applyId
        rr = app_get(f"{APP_URL}/app-api/dist/promoter/info", token)
        apply_id = None

    # 2. Admin 审核通过
    r = api_session.get(f"{ADMIN_URL}/admin-api/dist/promoter-apply/get",
                        headers=admin_headers, params={"id": apply_id}, verify=False).json()
    if r["code"] == 0 and r["data"] and r["data"].get("status") != 20:
        up = {**r["data"], "status": 20}
        api_session.put(f"{ADMIN_URL}/admin-api/dist/promoter-apply/update",
                        json=up, headers=admin_headers, verify=False)

    # 3. 实名认证
    auth = {"idCardFront": ID_CARD, "idCardBack": ID_CARD}
    app_post(f"{APP_URL}/app-api/dist/promoter/real-name-auth", auth, token)

    # 4. 签署协议
    app_post(f"{APP_URL}/app-api/dist/promoter/sign-agreement",
             {"agreementUrl": "https://example.com/signed.pdf"}, token)

    # 5. 获取 promoterId 校验
    r = app_get(f"{APP_URL}/app-api/dist/promoter/info", token)
    assert r["code"] == 0, f"获取推广员信息失败: {r}"
    assert int(r["data"]["promoterId"]) > 0, f"推广员认证失败: {r}"

    # 返回带鉴权 headers，供用例直接请求
    return {
        **Login.SMS_LOGIN_HEADERS,
        "timestamp": str(int(time.time() * 1000)),
        "Authorization": f"Bearer {token}",
    }

