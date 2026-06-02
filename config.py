# config.py
import os

# ======================
# 1. 环境配置 (Environment)
# ======================
ENV = os.getenv("TEST_ENV", "test")  # 默认使用 test 环境

BASE_URL = {
    "dev": "http://fenghuotai-dev.xxx.com/api/v1",
    "test": "http://fenghuotai-test.xxx.com/api/v1",
    "prod": "http://fenghuotai-prod.xxx.com/api/v1"
}

API_BASE_URL = BASE_URL[ENV]

# ======================
# 2. 账号配置 (Account)
# ======================
ACCOUNTS = {
    "admin": {  # 超级管理员，用于配置规则
        "username": "auto_admin",
        "password": "AutoTest@123"
    },
    "operator": {  # 运营人员，用于日常操作
        "username": "auto_operator",
        "password": "AutoTest@123"
    }
}

# ======================
# 3. 测试数据 ID (Data IDs)
# ======================
TEST_DATA_IDS = {
    # --- 区域与围栏 ---
    "region": {
        "henan_zhengzhou_jinshui": "REGION_ID_12345",  # 河南省-郑州市-金水区 (已开通)
        "henan_zhengzhou_erqi": "REGION_ID_67890"      # 河南省-郑州市-二七区 (未开通)
    },
    "fence": {
        "parent_fence_a": "FENCE_ID_PARENT_A",  # 父围栏A
        "child_fence_b": "FENCE_ID_CHILD_B"     # 子围栏B (在A内)
    },
    # --- 风控规则 ---
    "risk_rule": {
        "step_rule_limit_3": "RULE_ID_STEP_3",  # 阶梯规则：0-2正常，3+禁止下单
        "weight_rule_10kg": "RULE_ID_WEIGHT_10" # 重量规则：>10kg送检
    }
}

# ======================
# 4. 测试用户 (Test Users)
# ======================
TEST_USERS = {
    "whitelist_user": "USER_ID_WHITELIST_001",
    "blacklist_user": "USER_ID_BLACKLIST_001",
    "normal_user": "USER_ID_NORMAL_001"
}

# ======================
# 5. 数据库配置 (DB)
# ======================
DB_CONFIG = {
    "host": "test-db.xxx.com",
    "port": 3306,
    "user": "test_db_user",
    "password": "test_db_password",
    "database": "fenghuotai_test"
}