import json
import sys
import os
from datetime import date, timedelta

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from config import APP_URL
from Common.loader import load_yaml
from Common.login import Login
import requests

_WEEKDAY_MAP = {0: "周一", 1: "周二", 2: "周三", 3: "周四", 4: "周五", 5: "周六", 6: "周日"}

session = requests.Session()
session.headers.update({"Content-Type": "application/json", "User-Agent": "Mozilla/5.0"})
login_tool = Login(session)

orders = load_yaml("batch_orders.yaml")["batch_orders"]
users = load_yaml("batch_users.yaml")["batch_users"]
mobile_to_user = {u["mobile"]: u for u in users}

for order in orders:
    mobile = order["mobile"]
    user = mobile_to_user[mobile]
    token = login_tool.app_login(mobile=mobile)
    headers = {**Login.SMS_LOGIN_HEADERS, "Authorization": f"Bearer {token}"}

    tomorrow = date.today() + timedelta(days=1)
    payload = {
        "platform": "web",
        "provider": order["provider"],
        "bizMode": "WeightClothes",
        "userName": user["nickname"],
        "userPhone": mobile,
        "appointmentDate": tomorrow.strftime("%Y-%m-%d"),
        "appointmentTimePeriod": order["appointmentTimePeriod"],
        "appointmentWeekStr": _WEEKDAY_MAP[tomorrow.weekday()],
        "addressId": user["address"]["addressId"],
        "lat": order.get("lat", ""),
        "lon": order.get("lon", ""),
        "estimatedInfo": "10~30kg",
        "predictWeight": "10~30kg",
    }

    resp = session.post(f"{APP_URL}/app-api/recycle/order/v2/mini-order-submit", json=payload, headers=headers)
    print(f"=== {order['desc']} ({mobile}) ===")
    print("请求:", json.dumps(payload, ensure_ascii=False, indent=2))
    print("响应:", resp.text)
    print()
