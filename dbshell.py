"""微型 DB 交互工具，用法：
    python dbshell.py "SELECT count(*) as cnt FROM member_user"
    python dbshell.py "SELECT id, nickname, mobile FROM member_user LIMIT 5"
"""
import os, sys
os.environ["USE_MOCK"] = "false"  # 强制走真实 DB
from Common.DB import DBClient
sql = sys.argv[1] if len(sys.argv) > 1 else input("SQL> ")
with DBClient() as db:
    cursor = db.conn.cursor()
    cursor.execute(sql)
    rows = cursor.fetchall()
    cursor.close()
for i, r in enumerate(rows):
    print(f"[{i+1}] {r}")
print(f"\n--- {len(rows)} rows ---")
