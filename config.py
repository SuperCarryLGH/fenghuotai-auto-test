
import os

# ======================
# 1. 环境配置 (Environment)
# ======================
ENV = os.getenv("TEST_ENV", "dev")  # 默认使用 dev 环境

# ======================
# 2. 管理后台配置 (Admin)
#    地址 + 账号按环境绑定，TEST_ENV 切到哪就自动用哪套
# ======================
ADMIN_CONFIG = {
    "dev": {
        "base_url": "https://api-fht-dev.hengyishou.com",   # TODO 替换
        "accounts": {
            "admin": {"username": "autotest", "password": "1qaz!QAZ"},           # TODO 替换
            "operator": {"username": "auto_operator", "password": "AutoTest@123"},  # TODO 替换
        },
    },
    "test": {
        "base_url": "http://admin-test.xxx.com/api/v1",     # TODO 替换
        "accounts": {
            "admin": {"username": "auto_admin", "password": "AutoTest@123"},        # TODO 替换
            "operator": {"username": "auto_operator", "password": "AutoTest@123"},  # TODO 替换
        },
    },
    "prod": {
        "base_url": "http://admin-prod.xxx.com/api/v1",    # TODO 替换
        "accounts": {
            "admin": {"username": "auto_admin", "password": "AutoTest@123"},        # TODO 替换
            "operator": {"username": "auto_operator", "password": "AutoTest@123"},  # TODO 替换
        },
    },
}

ADMIN_URL = ADMIN_CONFIG[ENV]["base_url"]
ACCOUNTS = ADMIN_CONFIG[ENV]["accounts"]

# ======================
# 3. APP 用户端配置
# ======================
APP_CONFIG = {
    "dev": {
        "base_url": "https://api-fht-dev.hengyishou.com",
        "base_url_local": "http://192.168.0.138:48080",           # TODO 替换
        # TODO: 如果需要 APP 端专用账号，加在这里
        "accounts": {
            "normal_user": {"mobile": "15617617160", "code": "9999"},
        },
    },
    "test": {
        "base_url": "http://app-test.xxx.com/api/v1",          # TODO 替换
    },
    "prod": {
        "base_url": "https://api-fht.hengyishou.com",
    },
}

APP_URL = APP_CONFIG[ENV]["base_url"]

# ======================
# 4. 数据库配置 (DB)
# ======================
DB_CONFIG = {
    "host": "rm-bp1kmprsfdog024fsro.mysql.rds.aliyuncs.com",
    "port": 3306,
    "user": "sf_fht_dev",
    "password": "8HUvyZf6X&FNR%5",
    "database": "fht_yhs"
}