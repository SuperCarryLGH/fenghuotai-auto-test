"""
================================================================================
数据库工具模块 v2.0

【功能】
  - DBClient：封装 pymysql，提供 execute / fetch_one / fetch_all / insert / update / delete
  - Mock 模式 (USE_MOCK=true)：所有操作无痕通过，不连真实数据库
  - BizHelper：业务查询层，每个方法预留了 TODO SQL，填入真实表名和字段

【使用方式】
    from Common.DB import DBClient

    with DBClient() as db:
        order = db.fetch_one("SELECT * FROM orders WHERE order_no=%s", ("xxx",))

【重要：开始填数前要做的事】
  ☐ 1. 在 config.py 中填数据库连接
  ☐ 2. TODO 替换为表名/字段
  ☐ 3. 把 Date/ 下的 yaml 数据结构填完整
================================================================================
"""
import os
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Union

from pymysql import connect
from pymysql.cursors import DictCursor

USE_MOCK = os.getenv("USE_MOCK", "true").lower() in ("1", "true", "yes")


# ===================================================================
# 1. 异常定义
# ===================================================================
class DBError(Exception):
    """数据库操作异常"""


# ===================================================================
# 2. Mock 层（USE_MOCK=true 时使用，不连数据库）
# ===================================================================
class MockCursor:
    def __init__(self):
        self._rows: List[Dict] = []
        self.rowcount = 0
        self.lastrowid = 0

    def execute(self, sql: str, params: tuple = ()) -> int:  # noqa: ARG002
        return 0

    def fetchone(self) -> Optional[Dict]:
        return None

    def fetchall(self) -> List[Dict]:
        return []

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


class MockConnection:
    def __init__(self):
        self._cursor = MockCursor()

    def cursor(self) -> MockCursor:
        return self._cursor

    @staticmethod
    def commit():
        pass

    @staticmethod
    def rollback():
        pass

    @staticmethod
    def close():
        pass

    @staticmethod
    def begin():
        pass

    def __enter__(self):
        return self

    def __exit__(self, *args):
        pass


# ===================================================================
# 3. DBClient 核心类
# ===================================================================
class DBClient:
    """
    数据库客户端，支持普通模式与 Mock 模式。

    普通模式：每次 new 创建一个新连接，使用 with 自动关闭。
    Mock 模式：所有方法返回空结果，不发起真实网络请求。
    """

    def __init__(self, config: dict = None, force_mock: bool = False):
        self._config = config or {}
        self._force_mock = force_mock
        self._conn: Optional[Union["MockConnection", Any]] = None

    # -------------------- 连接管理 --------------------
    def _get_connection(self):
        """获取连接（首次调用时创建）"""
        if self._conn is not None:
            return self._conn

        if USE_MOCK or self._force_mock:
            self._conn = MockConnection()
            return self._conn

        from config import DB_CONFIG
        try:
            self._conn = connect(
                **DB_CONFIG,
                cursorclass=DictCursor,
                connect_timeout=5,
                charset="utf8mb4",
            )
        except Exception as e:
            raise DBError(f"数据库连接失败: {e}") from e

        return self._conn

    @property
    def conn(self):
        return self._get_connection()

    def close(self):
        if self._conn and not USE_MOCK:
            self._conn.close()
        self._conn = None

    # -------------------- 上下文管理器 --------------------
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    # -------------------- 核心查询方法 --------------------
    def execute(self, sql: str, params: tuple = ()) -> int:
        """执行 INSERT / UPDATE / DELETE，返回受影响行数"""
        with self.conn.cursor() as cur:
            cur.execute(sql, params)
            rowcount = cur.rowcount
        self.conn.commit()
        return rowcount

    def executemany(self, sql: str, params_list: List[tuple]) -> int:
        """批量执行，返回总受影响行数"""
        total = 0
        with self.conn.cursor() as cur:
            cur.executemany(sql, params_list)
            total = cur.rowcount
        self.conn.commit()
        return total

    def fetch_one(self, sql: str, params: tuple = ()) -> Optional[Dict]:
        """查询单条，返回 dict 或 None"""
        with self.conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchone()

    def fetch_all(self, sql: str, params: tuple = ()) -> List[Dict]:
        """查询多条，返回 list[dict]"""
        with self.conn.cursor() as cur:
            cur.execute(sql, params)
            return cur.fetchall()

    def insert(self, table: str, data: Dict) -> int:
        """
        简易插入，自动拼 INSERT INTO table (k1,k2) VALUES (%s,%s)
        返回自增 ID（如果表有 AUTO_INCREMENT）
        """
        cols = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        sql = f"INSERT INTO {table} ({cols}) VALUES ({placeholders})"
        with self.conn.cursor() as cur:
            cur.execute(sql, tuple(data.values()))
            last_id = cur.lastrowid
        self.conn.commit()
        return last_id

    def update(self, table: str, data: Dict, where: str, where_params: tuple = ()) -> int:
        """
        简易更新，自动拼 UPDATE table SET k1=%s, k2=%s WHERE ...
        data = {"field_name": new_value}
        """
        set_clause = ", ".join([f"{k}=%s" for k in data])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where}"
        params = tuple(data.values()) + where_params
        with self.conn.cursor() as cur:
            cur.execute(sql, params)
            rowcount = cur.rowcount
        self.conn.commit()
        return rowcount

    def delete(self, table: str, where: str, where_params: tuple = ()) -> int:
        """简易删除"""
        sql = f"DELETE FROM {table} WHERE {where}"
        with self.conn.cursor() as cur:
            cur.execute(sql, where_params)
            rowcount = cur.rowcount
        self.conn.commit()
        return rowcount

    # -------------------- 事务管理 --------------------
    def begin(self):
        self.conn.begin()

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    @contextmanager
    def transaction(self):
        """事务上下文，异常时自动回滚"""
        try:
            self.begin()
            yield self
            self.commit()
        except Exception:
            self.rollback()
            raise


# ===================================================================
# 4. 业务查询助手 —— 【TODO】把下方的 SQL 替换为真实表名/字段
# ===================================================================
class BizHelper:
    """
    业务查询层，按业务模块分类。
    每个方法就是一个 DSL，你只需要填参数，SQL 已经封装好。

    使用方法：
        with DBClient() as db:
            helper = BizHelper(db)
            order = helper.get_order_by_no("MOCK_ORDER_001")
    """

    def __init__(self, db: DBClient):
        self.db = db

    # ---------- 订单相关 ----------
    # TODO: 把 orders 替换成真实订单表名，字段名也按实际改
    ORDER_TABLE = "orders"

    def get_order_by_no(self, order_no: str) -> Optional[Dict]:
        """根据订单号查订单"""
        return self.db.fetch_one(
            f"SELECT * FROM {self.ORDER_TABLE} WHERE order_no = %s",  # TODO 确认字段名
            (order_no,),
        )

    def get_order_status(self, order_no: str) -> Optional[str]:
        """查订单状态"""
        row = self.db.fetch_one(
            f"SELECT status FROM {self.ORDER_TABLE} WHERE order_no = %s",  # TODO 确认字段名
            (order_no,),
        )
        return row["status"] if row else None

    # TODO: 按业务需要补充 order 相关查询
    # 例如：
    #   get_orders_by_user(user_id) -> List[Dict]
    #   get_orders_by_date(date) -> List[Dict]
    #   count_user_month_orders(user_id, year, month) -> int

    # ---------- 用户指标相关 ----------
    # TODO: 把 user_month_count 替换成真实表名
    USER_MONTH_TABLE = "user_month_count"

    def get_user_month_count(self, user_id: str) -> Optional[int]:
        return self.db.fetch_one(
            f"SELECT count FROM {self.USER_MONTH_TABLE} WHERE user_id = %s",  # TODO 确认字段
            (user_id,),
        )

    def reset_user_month_count(self, user_id: str):
        """将用户月下单次数清零"""
        self.db.update(
            self.USER_MONTH_TABLE,
            {"count": 0},  # TODO 确认字段名
            "user_id = %s",
            (user_id,),
        )

    # ---------- 规则绑定相关 ----------
    # TODO: 把 risk_rule_bind 替换成真实表名
    RISK_RULE_BIND_TABLE = "risk_rule_bind"

    def get_rule_bindings(self, region_id: str) -> List[Dict]:
        """查某区域绑定了哪些规则"""
        return self.db.fetch_all(
            f"SELECT * FROM {self.RISK_RULE_BIND_TABLE} WHERE region_id = %s",  # TODO 确认字段
            (region_id,),
        )

    # ---------- 风控日志相关 ----------
    # TODO: 把 risk_check_log 替换成真实表名
    RISK_LOG_TABLE = "risk_check_log"

    def get_risk_log_by_order(self, order_no: str) -> Optional[Dict]:
        """查某订单的风控检查记录"""
        return self.db.fetch_one(
            f"SELECT * FROM {self.RISK_LOG_TABLE} WHERE order_no = %s",  # TODO 确认字段
            (order_no,),
        )

    # ---------- 围栏相关 ----------
    # TODO: 把 fence 替换成真实表名
    FENCE_TABLE = "fence"

    def get_fence_by_id(self, fence_id: str) -> Optional[Dict]:
        return self.db.fetch_one(
            f"SELECT * FROM {self.FENCE_TABLE} WHERE id = %s",  # TODO 确认字段
            (fence_id,),
        )

    # ---------- 数据清理（测试用） ----------
    # TODO: 补充所有需要清理的测试数据表
    TEST_TABLES = {
        "orders": "is_test = 1",         # TODO 确认测试标记字段
        "risk_check_log": "is_test = 1", # TODO 同上
    }

    def clean_test_data(self):
        """清理测试产生的垃圾数据"""
        for table, where in self.TEST_TABLES.items():
            self.db.delete(table, where)

    # ---------- 通用工具 ----------
    def table_exists(self, table_name: str) -> bool:
        """检查表是否存在（方便你调试时确认表名）"""
        row = self.db.fetch_one(
            "SELECT TABLE_NAME FROM information_schema.TABLES "
            "WHERE TABLE_SCHEMA = DATABASE() AND TABLE_NAME = %s",
            (table_name,),
        )
        return row is not None


# ===================================================================
# 5. 便捷函数（不用 import 类，直接调用）
# ===================================================================
def get_db(config: dict = None) -> DBClient:
    """快速获取一个 DBClient 实例"""
    return DBClient(config)


def quick_query(sql: str, params: tuple = ()) -> Union[Optional[Dict], List[Dict]]:
    """快速执行一条查询，自动管理连接（适合在脚本里用）"""
    with DBClient() as db:
        sql_stripped = sql.strip().upper()
        if sql_stripped.startswith("SELECT"):
            if "LIMIT 1" in sql_stripped or "WHERE id =" in sql_stripped:
                return db.fetch_one(sql, params)
            return db.fetch_all(sql, params)
        return db.execute(sql, params)
