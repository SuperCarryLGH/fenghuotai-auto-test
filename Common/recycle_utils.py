"""回收清运链路工具：从用户下单到清运单创建的完整流程封装"""
import datetime
import time
import requests
from config import APP_URL, ADMIN_URL
from Common.login import Login


class RecycleChain:
    """清运链路构建器

    完整流程（均已对 dev 实测验证）：
      用户下单(到站点) → 站点B端接单 → 称重(≥1000kg累计) → 支付
      → 站点B端呼叫清运(call-clean-now) → 生成清运单并自动关联订单
    之后由司机B端执行：accept → depart → arrive → update-weight → weighing-complete → loading-complete

    角色账号（B端 system_users，走 /admin-api/system/auth/sms-login）：
      站点: 18600000010（同乐站点，司机所属站点）
      司机: 18600000001（driver01 李运）
    """

    STATION_ID = 2061713873303195650          # 同乐站点（司机所属）
    STATION_NAME = "同乐站点"
    STATION_MOBILE = "18600000010"            # 同乐站点运营 B端账号
    DRIVER_MOBILE = "18600000001"             # 司机 B端账号
    DRIVER_ID = "2054374957553369090"         # driver01 李运 system_users id
    WEIGHER_MOBILE = "18600000003"            # 司磅员 B端账号(sibang01 张一)
    USER_MOBILE = "15617637160"               # C端下单用户
    WAREHOUSE_ID = 4
    OPERATION_CENTER_ID = 2074701657159761922
    ERP_PRODUCT_TONGHUO = 2047530778823024642  # 统货 erp 产品 id（司机称重用）

    def __init__(self, api_session=None):
        self.s = api_session or requests.Session()
        self.s.verify = False
        self.s.headers.update({
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
                          "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0",
            "Content-Type": "application/json",
        })
        self.login = Login(session=self.s)

    # ------------------------------------------------------------------
    # 基础
    # ------------------------------------------------------------------
    def _b_login(self, mobile, code="9999"):
        """B端（system_users）短信登录"""
        r = self.s.post(f"{ADMIN_URL}/admin-api/system/auth/sms-login",
                        json={"mobile": mobile, "code": code},
                        headers={"tenant-id": "1", "appId": "admin", "sign": "admin"},
                        timeout=20)
        r.raise_for_status()
        data = r.json()
        assert data["code"] == 0, f"B端登录失败 {mobile}: {data.get('msg')}"
        return data["data"]["accessToken"]

    def _b_headers(self, token):
        return {"tenant-id": "1", "appId": "admin", "sign": "admin",
                "Authorization": f"Bearer {token}"}

    def _c_headers(self, token):
        return {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}

    def _post(self, url, payload, headers):
        resp = self.s.post(url, json=payload, headers=headers, timeout=20)
        data = resp.json()
        assert data["code"] == 0, f"POST {url} 失败: code={data.get('code')} msg={data.get('msg')}"
        return data

    def _get(self, url, params, headers):
        resp = self.s.get(url, params=params, headers=headers, timeout=20)
        data = resp.json()
        assert data["code"] == 0, f"GET {url} 失败: code={data.get('code')} msg={data.get('msg')}"
        return data

    # ------------------------------------------------------------------
    # 完整链路：下单 → 接单 → 称重 → 支付 → 呼叫清运
    # 返回 (clear_order_id, order_id, station_token, driver_token, user_token)
    # ------------------------------------------------------------------
    def build_chain(self, weight=1500):
        user_token = self.login.app_login_with(mobile=self.USER_MOBILE, code="9999")
        station_token = self._b_login(self.STATION_MOBILE)
        driver_token = self._b_login(self.DRIVER_MOBILE)

        today = datetime.date.today().strftime("%Y-%m-%d")
        wd = {0: "周一", 1: "周二", 2: "周三", 3: "周四", 4: "周五", 5: "周六", 6: "周日"}[datetime.date.today().weekday()]

        # 1. 用户下单到同乐站点
        r = self._post(f"{APP_URL}/app-api/recycle/order/station-order-submit", {
            "platform": "web", "provider": "", "scene": "", "lat": 23.129163, "lon": 113.264435,
            "itemId": "", "pics": "", "promoterId": "", "promotionPlatform": "", "promotionChannel": "",
            "promotionStationId": "", "activityId": "", "payType": 2,
            "stationId": self.STATION_ID, "name": self.STATION_NAME,
            "mobile": self.USER_MOBILE, "predictWeight": 50000025,
        }, self._c_headers(user_token))
        order_id = r["data"]["id"]
        time.sleep(1)

        # 2. 站点接单
        self._post(f"{ADMIN_URL}/admin-api/recycle/app-order/receive", {
            "orderId": order_id, "status": 21, "payType": 2, "payPrice": 12.5, "phoneTailFour": "7160",
        }, self._b_headers(station_token))
        time.sleep(1)

        # 3. 称重 + 支付
        d = self._get(f"{ADMIN_URL}/admin-api/recycle/app-order/get-order-info",
                      {"id": order_id}, self._b_headers(station_token))["data"]
        item_id = (d.get("recycleOrderItemRespVos") or [{}])[0].get("id")
        assert item_id, "订单无品类明细"
        self._post(f"{ADMIN_URL}/admin-api/recycle/app-order/order-weighting", {
            "orderId": order_id, "recycleOrderItemId": item_id, "price": 2.5, "weight": weight,
        }, self._b_headers(station_token))
        time.sleep(1)
        self._post(f"{ADMIN_URL}/admin-api/recycle/app-order/pay-order", {
            "orderId": order_id, "payPrice": weight * 2.5, "payType": 2,
        }, self._b_headers(station_token))
        time.sleep(2)

        # 4. 呼叫清运（站点累计重量需 ≥1000kg，单笔 weight 传大值保证）
        r = self._post(f"{ADMIN_URL}/admin-api/recycle/app-order/call-clean-now", {
            "stationId": self.STATION_ID, "warehouseId": self.WAREHOUSE_ID,
            "operationCenterId": self.OPERATION_CENTER_ID,
            "appointmentDate": today, "appointmentTimePeriod": "10:00-11:00",
            "appointmentWeekStr": wd, "clearType": 1, "clearTarget": 2,
        }, self._b_headers(station_token))
        clear_order_id = r["data"]["id"]
        time.sleep(1)
        return clear_order_id, order_id, station_token, driver_token, user_token

    # ------------------------------------------------------------------
    # 司机链路
    # ------------------------------------------------------------------
    def driver_accept(self, clear_order_id, driver_token):
        return self._post(f"{ADMIN_URL}/admin-api/recycle/app-clearOrder-driver/accept",
                          {"id": clear_order_id}, self._b_headers(driver_token))

    def driver_get(self, clear_order_id, driver_token):
        return self._get(f"{ADMIN_URL}/admin-api/recycle/app-clearOrder-driver/get",
                         {"id": clear_order_id}, self._b_headers(driver_token))

    def driver_cancel(self, clear_order_id, driver_token):
        return self._post(f"{ADMIN_URL}/admin-api/recycle/app-clearOrder-driver/cancel",
                          {"id": clear_order_id}, self._b_headers(driver_token))

    def driver_depart(self, clear_order_id, driver_token):
        return self._post(f"{ADMIN_URL}/admin-api/recycle/app-clearOrder-driver/depart",
                          {"id": clear_order_id}, self._b_headers(driver_token))

    def driver_arrive(self, clear_order_id, driver_token):
        return self._post(f"{ADMIN_URL}/admin-api/recycle/app-clearOrder-driver/arrive",
                          {"id": clear_order_id}, self._b_headers(driver_token))

    def driver_weigh(self, clear_order_id, driver_token, package_no=None, item_id=None, weight=100):
        package_no = package_no or f"CL{int(time.time() * 1000)}"
        return self._post(f"{ADMIN_URL}/admin-api/recycle/app-clearOrder-driver/update-weight", {
            "clearOrderId": clear_order_id, "packageNo": package_no,
            "itemId": item_id or self.ERP_PRODUCT_TONGHUO, "weight": weight,
        }, self._b_headers(driver_token))

    def driver_weighing_complete(self, clear_order_id, driver_token):
        return self._post(f"{ADMIN_URL}/admin-api/recycle/app-clearOrder-driver/weighing-complete",
                          {"id": clear_order_id}, self._b_headers(driver_token))

    def driver_loading_complete(self, clear_order_id, driver_token):
        return self._post(f"{ADMIN_URL}/admin-api/recycle/app-clearOrder-driver/loading-complete",
                          {"id": clear_order_id}, self._b_headers(driver_token))

    # ------------------------------------------------------------------
    # 司机完整链路（到装车完成/待到厂，供称重员后续操作）
    # ------------------------------------------------------------------
    def driver_full_chain(self, clear_order_id, driver_token):
        self.driver_accept(clear_order_id, driver_token)
        time.sleep(1)
        self.driver_depart(clear_order_id, driver_token)
        time.sleep(1)
        self.driver_arrive(clear_order_id, driver_token)
        time.sleep(1)
        self.driver_weigh(clear_order_id, driver_token)
        time.sleep(1)
        self.driver_weighing_complete(clear_order_id, driver_token)
        time.sleep(1)
        self.driver_loading_complete(clear_order_id, driver_token)
        time.sleep(1)

    # ------------------------------------------------------------------
    # 称重员操作
    # ------------------------------------------------------------------
    def weigher_login(self):
        return self._b_login(self.WEIGHER_MOBILE)

    def weigher_scan_stockin(self, clear_order_id, weigher_token):
        package = self._get_first_package(clear_order_id)
        assert package, f"清运单 {clear_order_id} 无包裹可入库"
        return self._post(f"{ADMIN_URL}/admin-api/recycle/app-clearOrder-weigher/scan-stockin", {
            "packageNo": package["package_no"], "id": package["id"],
            "fileUrls": ["https://example.com/stockin.jpg"], "weight": package.get("recycle_weight") or 0,
            "warehouseId": self.WAREHOUSE_ID,
        }, self._b_headers(weigher_token))

    def weigher_stockin_fullvehicle(self, clear_order_id, weigher_token):
        return self._post(f"{ADMIN_URL}/admin-api/recycle/app-clearOrder-weigher/stockin-fullvehicle",
                          {"id": clear_order_id}, self._b_headers(weigher_token))

    def _get_first_package(self, clear_order_id):
        """查清运单的包裹（recycle_package_item）"""
        import os
        import pymysql
        conn = pymysql.connect(host=os.getenv("DB_HOST"), port=int(os.getenv("DB_PORT", "3306")),
            user=os.getenv("DB_USER"), password=os.getenv("DB_PASSWORD", ""),
            database=os.getenv("DB_DATABASE"), connect_timeout=5, charset="utf8mb4")
        try:
            with conn.cursor() as cur:
                cur.execute(
                    "SELECT id, package_no, recycle_weight FROM recycle_package_item "
                    "WHERE clear_order_id=%s AND deleted=0 LIMIT 1", (clear_order_id,))
                row = cur.fetchone()
                return {"id": row[0], "package_no": row[1], "recycle_weight": row[2]} if row else None
        finally:
            conn.close()

    # ------------------------------------------------------------------
    # 站点订单阶段（app-order 接口，站点 B端 操作）
    # ------------------------------------------------------------------
    def station_login(self):
        return self._b_login(self.STATION_MOBILE)

    def create_order(self, user_token, station_id=None, station_name=None, weight=1500, user_mobile=None):
        """用户下单到站点，返回 order_id 与 item_id"""
        user_mobile = user_mobile or self.USER_MOBILE
        station_id = station_id or self.STATION_ID
        station_name = station_name or self.STATION_NAME
        r = self._post(f"{APP_URL}/app-api/recycle/order/station-order-submit", {
            "platform": "web", "provider": "", "scene": "", "lat": 23.129163, "lon": 113.264435,
            "itemId": "", "pics": "", "promoterId": "", "promotionPlatform": "", "promotionChannel": "",
            "promotionStationId": "", "activityId": "", "payType": 2,
            "stationId": station_id, "name": station_name,
            "mobile": user_mobile, "predictWeight": 50000025,
        }, self._c_headers(user_token))
        order_id = r["data"]["id"]
        time.sleep(1)
        return order_id

    def order_receive(self, order_id, station_token, phone_tail="7160"):
        r = self._post(f"{ADMIN_URL}/admin-api/recycle/app-order/receive", {
            "orderId": order_id, "status": 21, "payType": 2, "payPrice": 12.5, "phoneTailFour": phone_tail,
        }, self._b_headers(station_token))
        time.sleep(1)
        return r

    def order_get_item_id(self, order_id, station_token):
        d = self._get(f"{ADMIN_URL}/admin-api/recycle/app-order/get-order-info",
                      {"id": order_id}, self._b_headers(station_token))["data"]
        item_id = (d.get("recycleOrderItemRespVos") or [{}])[0].get("id")
        assert item_id, "订单无品类明细"
        return item_id

    def order_weigh(self, order_id, item_id, station_token, weight=1500):
        r = self._post(f"{ADMIN_URL}/admin-api/recycle/app-order/order-weighting", {
            "orderId": order_id, "recycleOrderItemId": item_id, "price": 2.5, "weight": weight,
        }, self._b_headers(station_token))
        time.sleep(1)
        return r

    def order_pay(self, order_id, station_token, weight=1500):
        r = self._post(f"{ADMIN_URL}/admin-api/recycle/app-order/pay-order", {
            "orderId": order_id, "payPrice": weight * 2.5, "payType": 2,
        }, self._b_headers(station_token))
        time.sleep(2)
        return r

    def order_call_clean(self, order_id, station_token):
        today = datetime.date.today().strftime("%Y-%m-%d")
        wd = {0: "周一", 1: "周二", 2: "周三", 3: "周四", 4: "周五", 5: "周六", 6: "周日"}[datetime.date.today().weekday()]
        r = self._post(f"{ADMIN_URL}/admin-api/recycle/app-order/call-clean-now", {
            "stationId": self.STATION_ID, "warehouseId": self.WAREHOUSE_ID,
            "operationCenterId": self.OPERATION_CENTER_ID,
            "appointmentDate": today, "appointmentTimePeriod": "10:00-11:00",
            "appointmentWeekStr": wd, "clearType": 1, "clearTarget": 2,
        }, self._b_headers(station_token))
        time.sleep(1)
        return r

    # ------------------------------------------------------------------
    # 站点线索
    # ------------------------------------------------------------------
    def create_clue(self, admin_headers, name=None, user_id=1, user_name="admin"):
        """创建站点线索，返回 (clue_id, clue_no)

        :param admin_headers: 管理后台鉴权头（需含登录用户的 tenant/appId/sign/Authorization）
        :param name: 线索名字（可空，自动生成）
        :param user_id: 维护人 id（必填，来自当前登录用户）
        :param user_name: 维护人名字（必填）
        """
        name = name or f"autotest_clue_{int(time.time() * 1000)}"
        clue_no = f"SC{int(time.time() * 1000)}"
        r = self._post(f"{ADMIN_URL}/admin-api/recycle/station/clue/create", {
            "clueNo": clue_no,
            "poolType": 0, "clueName": name, "stationType": 1,
            "userId": user_id, "userName": user_name,
            "receiveUserId": user_id, "receiveUserName": user_name,
            "status": 20, "visitCount": 0,
            "provinceCode": "330000", "province": "浙江省",
            "cityCode": "330100", "city": "杭州市",
            "districtCode": "330108", "district": "滨江区",
            "detailAddress": "测试地址",
        }, admin_headers)
        data = r.get("data")
        clue_id = data.get("id") if isinstance(data, dict) else data
        clue_no = data.get("clueNo") or data.get("clue_no") or clue_no if isinstance(data, dict) else clue_no
        if not clue_no:
            try:
                detail = self._get(f"{ADMIN_URL}/admin-api/recycle/station/clue/get",
                                   {"id": clue_id}, admin_headers).get("data") or {}
                clue_no = detail.get("clueNo") or ""
            except Exception:
                pass
        return clue_id, clue_no
