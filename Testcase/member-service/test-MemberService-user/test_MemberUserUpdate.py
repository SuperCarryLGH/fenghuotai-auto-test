import pytest
from config import ADMIN_URL


class TestMemberUserUpdate:
    """更新会员用户"""

    @pytest.mark.smoke
    def test_MemberUserUpdate(self, api_session,auth_headers):
        """
        运行: TEST_ENV=dev USE_MOCK=false pytest ... -v -s
        """
        url = f"{ADMIN_URL}/admin-api/member/user/update"
        params = {
            "mobile": "", #手机号
            "status": "", #状态
            "nickname": "", #用户昵称
            "password": "",
            "avatar": "", #头像
            "name": "", #用户昵称
            "sex": "", #用户性别
            "areaId": "", #所在地编号
            "areaName": "", #所在地全称
            "birthday": "", #出生日期
            "mark": "", #会员备注
            "tagIds": "", #会员标签
            "levelId": "", #会员等级编号
            "groupId": "", #用户分组编号
            "platform": "", #
            "channel": "", #注册来源渠道
            "scene": "", #注册来源场景
            "riskStatus": "", #风控状态 0-正常 1-白名单 2-黑名单
            "riskLevel": "", #风控等级 0-无 1-低 2-中 3-高
            "superiorPromoterId": "", #上级推广员ID
            "superSuperiorPromoterId": "", #上上级推广员ID
            "promotionSiteId": "", #推广站点ID
            "promotionActivityId": "", #推广活动ID
            "isPromoter": "", #是否是推广员 0-否 1-是
            "wxTransferOpenid": "", #
            "aliTransferOpenid": "", #
            "aliTransferName": "", #
            "aliTransferMobile": "", #
            "operationCenterId": "", #运营中心id
            "id": "", #编号
            }

        resp = api_session.put(url, headers=auth_headers,json=params)
        assert resp.status_code == 200
        r = resp.json()
        assert r["code"] == 0
        #assert r["data"] == {}
        print(r)








#test_AppApiCooperationGetByPlatform