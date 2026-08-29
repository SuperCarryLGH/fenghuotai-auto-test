"""
顺丰费用回调接口 - 手动调用

使用方式:
  # 单次调用（手动输入）
  python sf_fee_push_call.py

  # 从文件批量调用（每5秒一次）
  python sf_fee_push_call.py --file sf_fee_push_data.json --interval 5

  # 仅预览，不实际调用
  python sf_fee_push_call.py --file sf_fee_push_data.json --dry-run
"""
import sys
import os
import json
import re
import time

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))
sys.path.insert(0, PROJECT_ROOT)

import requests
from config import APP_URL

ENDPOINT = f"{APP_URL}/app-api/recycle/express/fee-push/sf"


def parse_input(raw: str) -> tuple:
    """
    解析输入内容，返回 (content, sign)

    支持格式:
      1. 纯 JSON: {"orderNo":"PO202608281313431",...}
      2. Java Map格式: ({sign=..., content={...}})
      3. sign + content格式: sign=..., content={"orderNo":...}
    """
    raw = raw.strip()

    # 格式1: 纯 JSON（以 { 开头）
    if raw.startswith("{"):
        return raw, None

    # 格式2: Java Map格式 ({sign=..., content={...}})
    if raw.startswith("({") or raw.startswith("({"):
        sign_match = re.search(r'sign=(\S+?)[,\s}]', raw)
        sign = sign_match.group(1) if sign_match else None

        content_match = re.search(r'content=(\{.*\})\s*}', raw, re.DOTALL)
        if content_match:
            return content_match.group(1), sign

        content_match = re.search(r'content=(\{.*?\})', raw, re.DOTALL)
        if content_match:
            return content_match.group(1), sign

    # 格式3: sign=xxx, content={...}
    if "content=" in raw:
        sign_match = re.search(r'sign=(\S+?)[,\s]', raw)
        sign = sign_match.group(1) if sign_match else None

        content_match = re.search(r'content=(\{.*\})', raw, re.DOTALL)
        if content_match:
            return content_match.group(1), sign

    return raw, None


def sf_sign(content: str, checkword: str) -> str:
    """顺丰回调签名"""
    import hashlib
    import base64
    raw = f"{content}{checkword}".encode()
    return base64.b64encode(hashlib.md5(raw).digest()).decode()


def post(content: str, sign: str = None) -> dict:
    try:
        data = {"content": content}
        if sign:
            data["sign"] = sign

        resp = requests.post(
            ENDPOINT,
            data=data,
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "User-Agent": "Mozilla/5.0",
            },
            timeout=30,
        )
        return {"status": resp.status_code, "body": resp.json() if resp.status_code == 200 else resp.text}
    except Exception as e:
        return {"status": -1, "body": str(e)}


def load_json_file(file_path: str) -> list:
    """
    从 JSON 文件加载数据
    
    文件格式:
    [
      {"content": "{...}", "sign": "..."},
      ...
    ]
    """
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    # 验证格式
    if not isinstance(data, list):
        raise ValueError("JSON 文件格式错误：应为数组格式")
    
    for i, item in enumerate(data):
        if 'content' not in item:
            raise ValueError(f"第 {i+1} 条数据缺少 'content' 字段")
    
    return data


def batch_push(file_path: str, interval: int = 5, dry_run: bool = False):
    """
    批量推送
    
    参数:
        file_path: JSON 数据文件路径
        interval: 调用间隔（秒）
        dry_run: 仅预览，不实际调用
    """
    data = load_json_file(file_path)
    total = len(data)
    
    print("=" * 60)
    print(f"顺丰费用回调 - 批量推送")
    print("=" * 60)
    print(f"数据文件: {file_path}")
    print(f"数据条数: {total}")
    print(f"调用间隔: {interval}s")
    print(f"模式: {'预览（不调用）' if dry_run else '实际调用'}")
    print(f"接口地址: {ENDPOINT}")
    print("=" * 60)
    
    success_count = 0
    fail_count = 0
    results = []
    
    for i, item in enumerate(data, 1):
        content = item['content']
        sign = item.get('sign', '')
        
        # 解析 content 获取订单号
        try:
            parsed = json.loads(content)
            order_no = parsed.get('orderNo', '未知')
            waybill_no = parsed.get('waybillNo', '未知')
        except:
            order_no = '解析失败'
            waybill_no = '解析失败'
        
        print(f"\n[{i}/{total}] 订单: {order_no}, 运单: {waybill_no}")
        
        if dry_run:
            print(f"  [预览] 跳过实际调用")
            results.append({
                "index": i,
                "order_no": order_no,
                "waybill_no": waybill_no,
                "status": "preview",
                "message": "预览模式，未调用"
            })
            continue
        
        # 实际调用
        print(f"  发送中...")
        result = post(content, sign)
        
        if result['status'] == 200:
            body = result['body']
            if isinstance(body, dict) and body.get('code') == 0:
                print(f"  ✅ 成功")
                success_count += 1
                results.append({
                    "index": i,
                    "order_no": order_no,
                    "waybill_no": waybill_no,
                    "status": "success",
                    "message": "调用成功"
                })
            else:
                error_msg = body.get('msgData', '未知错误') if isinstance(body, dict) else str(body)
                print(f"  ❌ 失败: {error_msg}")
                fail_count += 1
                results.append({
                    "index": i,
                    "order_no": order_no,
                    "waybill_no": waybill_no,
                    "status": "fail",
                    "message": error_msg
                })
                # 失败时停止
                print(f"\n⚠️ 调用失败，停止执行")
                break
        else:
            print(f"  ❌ HTTP错误: {result['status']} - {result['body']}")
            fail_count += 1
            results.append({
                "index": i,
                "order_no": order_no,
                "waybill_no": waybill_no,
                "status": "error",
                "message": f"HTTP {result['status']}: {result['body']}"
            })
            # 失败时停止
            print(f"\n⚠️ 调用失败，停止执行")
            break
        
        # 等待间隔
        if i < total and not dry_run:
            print(f"  等待 {interval}s...")
            time.sleep(interval)
    
    # 打印汇总
    print("\n" + "=" * 60)
    print("执行汇总")
    print("=" * 60)
    print(f"总条数: {total}")
    print(f"成功: {success_count}")
    print(f"失败: {fail_count}")
    print(f"跳过: {total - success_count - fail_count}")
    print()
    
    # 打印详细结果
    print("详细结果:")
    for r in results:
        icon = "✅" if r['status'] == 'success' else ("❌" if r['status'] in ('fail', 'error') else "⏭️")
        print(f"  {icon} [{r['index']}] {r['order_no']} - {r['message']}")
    
    print("=" * 60)


def single_push():
    """单次调用（手动输入）"""
    print(f"接口: {ENDPOINT}")
    print("请输入回调内容（支持纯JSON、Java日志格式、sign+content格式）:")
    print("-" * 40)
    raw = input().strip()
    print("-" * 40)

    if not raw:
        print("内容为空，退出")
        sys.exit(1)

    content, sign = parse_input(raw)

    try:
        parsed = json.loads(content)
        print(f"\n解析成功:")
        print(f"  content: {json.dumps(parsed, ensure_ascii=False)[:200]}...")
        if sign:
            print(f"  sign: {sign}")
    except json.JSONDecodeError as e:
        print(f"\n⚠️ JSON解析失败: {e}")
        print(f"  原始内容: {content[:200]}")

    print(f"\n发送中...")
    result = post(content, sign)
    print(f"status: {result['status']}")
    print(f"响应: {json.dumps(result['body'], ensure_ascii=False, indent=2) if isinstance(result['body'], dict) else result['body']}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="顺丰费用回调接口 - 手动调用")
    parser.add_argument("--file", type=str, help="从 JSON 文件批量调用")
    parser.add_argument("--interval", type=int, default=5, help="批量调用间隔（秒），默认5")
    parser.add_argument("--dry-run", action="store_true", help="仅预览，不实际调用")
    
    args = parser.parse_args()
    
    if args.file:
        # 批量调用模式
        if not os.path.exists(args.file):
            print(f"❌ 文件不存在: {args.file}")
            sys.exit(1)
        batch_push(args.file, args.interval, args.dry_run)
    else:
        # 单次调用模式
        single_push()
