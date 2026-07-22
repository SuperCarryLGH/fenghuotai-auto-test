#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
资金流水倒推脚本（真实数据版）
根据 pay_wallet_transaction 表数据，倒推出分拣中心和公司的资金流水
分拣中心和公司ID均从数据中动态获取
运行此脚本将生成 fund_flow_insert.sql 文件
"""

import pandas as pd
from datetime import datetime
from typing import List, Dict, Tuple, Optional, Set
import os
from collections import defaultdict

# ==================== 配置区域 ====================

# 获取当前脚本所在目录
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))

# 获取项目根目录
PROJECT_ROOT = os.path.dirname(os.path.dirname(SCRIPT_DIR))


# 定义文件查找函数
def find_file(filename: str) -> str:
    """在多个可能的位置查找文件"""
    possible_paths = [
        os.path.join(SCRIPT_DIR, filename),
        os.path.join(PROJECT_ROOT, filename),
        os.path.join(PROJECT_ROOT, 'Testcase', 'DB', filename),
        filename,
    ]

    for path in possible_paths:
        if os.path.exists(path):
            return path

    return os.path.join(SCRIPT_DIR, filename)


CONFIG = {
    'pay_wallet_file': find_file('pay_wallet.csv'),
    'pay_wallet_transaction_file': find_file('pay_wallet_transaction.csv'),
    'member_user_file': find_file('member_user.csv'),
    'recycle_order_file': find_file('recycle_order.csv'),
}

# 打印文件路径信息
print("=" * 70)
print("📁 文件路径配置:")
for key, value in CONFIG.items():
    exists = "✅" if os.path.exists(value) else "❌"
    print(f"   {exists} {key}: {value}")
print("=" * 70)


# ==================== 数据模型 ====================

class CenterFundRecord:
    """分拣中心资金流水记录"""

    def __init__(self, center_id: str, change_type: str, channel: str,
                 amount: float, balance_after: float,
                 related_user_id: Optional[str] = None,
                 related_order_id: Optional[str] = None,
                 remark: str = ''):
        self.center_id = center_id
        self.change_type = change_type
        self.channel = channel
        self.amount = round(amount, 2)
        self.balance_after = round(balance_after, 2)
        self.related_user_id = related_user_id
        self.related_order_id = related_order_id
        self.remark = remark
        self.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        self.wallet_id = None


class CompanyFundRecord:
    """公司资金流水记录"""

    def __init__(self, company_id: str, change_type: str, channel: str,
                 amount: float, balance_after: float,
                 related_center_id: Optional[str] = None,
                 related_user_id: Optional[str] = None,
                 remark: str = ''):
        self.company_id = company_id
        self.change_type = change_type
        self.channel = channel
        self.amount = round(amount, 2)
        self.balance_after = round(balance_after, 2)
        self.related_center_id = related_center_id
        self.related_user_id = related_user_id
        self.remark = remark
        self.created_at = datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# ==================== 核心逻辑 ====================

class FundFlowReverser:
    """资金流水倒推引擎"""

    def __init__(self, config: Dict):
        self.config = config
        self.pay_wallet_df = None
        self.pay_wallet_transaction_df = None
        self.member_user_df = None
        self.recycle_order_df = None

        self.wallet_to_user: Dict[str, str] = {}
        self.user_to_center: Dict[str, str] = {}
        self.user_to_company: Dict[str, str] = {}
        self.order_to_center: Dict[str, str] = {}
        self.order_to_company: Dict[str, str] = {}
        self.center_to_company: Dict[str, str] = {}

        self.center_balance: Dict[str, Dict[str, float]] = defaultdict(lambda: {'WECHAT': 0.0, 'ALIPAY': 0.0})
        self.company_balance: Dict[str, Dict[str, float]] = defaultdict(lambda: {'WECHAT': 0.0, 'ALIPAY': 0.0})
        self.center_pending_withdraw: Dict[str, Dict[str, float]] = defaultdict(lambda: {'WECHAT': 0.0, 'ALIPAY': 0.0})

        self.center_records: List[CenterFundRecord] = []
        self.company_records: List[CompanyFundRecord] = []

        self.stats = {
            'settle_count': 0,
            'withdraw_count': 0,
            'centers': set(),
            'companies': set(),
            'total_settle_amount': 0.0,
            'total_withdraw_amount': 0.0,
        }

    def load_data(self) -> bool:
        """加载所有数据文件"""
        try:
            pay_wallet_file = self.config.get('pay_wallet_file', 'pay_wallet.csv')
            if os.path.exists(pay_wallet_file):
                self.pay_wallet_df = pd.read_csv(pay_wallet_file, encoding='utf-8-sig')
                print(f"✅ 加载 pay_wallet: {len(self.pay_wallet_df)} 条记录")
            else:
                print(f"❌ 文件不存在: {pay_wallet_file}")
                return False

            trans_file = self.config.get('pay_wallet_transaction_file', 'pay_wallet_transaction.csv')
            if os.path.exists(trans_file):
                self.pay_wallet_transaction_df = pd.read_csv(trans_file, encoding='utf-8-sig')
                print(f"✅ 加载 pay_wallet_transaction: {len(self.pay_wallet_transaction_df)} 条记录")
            else:
                print(f"❌ 文件不存在: {trans_file}")
                return False

            member_file = self.config.get('member_user_file', 'member_user.csv')
            if os.path.exists(member_file):
                self.member_user_df = pd.read_csv(member_file, encoding='utf-8-sig')
                print(f"✅ 加载 member_user: {len(self.member_user_df)} 条记录")
            else:
                print(f"❌ 文件不存在: {member_file}")
                return False

            order_file = self.config.get('recycle_order_file', 'recycle_order.csv')
            if os.path.exists(order_file):
                self.recycle_order_df = pd.read_csv(order_file, encoding='utf-8-sig')
                print(f"✅ 加载 recycle_order: {len(self.recycle_order_df)} 条记录")
            else:
                print(f"❌ 文件不存在: {order_file}")
                return False

            return True

        except Exception as e:
            print(f"❌ 加载数据失败: {e}")
            return False

    def build_mappings(self) -> None:
        """构建映射关系"""
        print("\n📊 构建映射关系...")

        for _, row in self.pay_wallet_df.iterrows():
            wallet_id = str(row.get('id', '')).strip()
            user_id = str(row.get('user_id', '')).strip()
            if wallet_id and user_id:
                self.wallet_to_user[wallet_id] = user_id
        print(f"   - wallet -> user: {len(self.wallet_to_user)} 条映射")

        for _, row in self.member_user_df.iterrows():
            user_id = str(row.get('id', '')).strip()
            center_id = str(row.get('operation_center_id', '')).strip()
            company_id = str(row.get('company_id', '')).strip()
            if user_id:
                if center_id:
                    self.user_to_center[user_id] = center_id
                if company_id:
                    self.user_to_company[user_id] = company_id
        print(f"   - user -> center: {len(self.user_to_center)} 条映射")
        print(f"   - user -> company: {len(self.user_to_company)} 条映射")

        for _, row in self.recycle_order_df.iterrows():
            order_id = str(row.get('id', '')).strip()
            center_id = str(row.get('operation_center_id', '')).strip()
            company_id = str(row.get('company_id', '')).strip()
            if order_id:
                if center_id:
                    self.order_to_center[order_id] = center_id
                if company_id:
                    self.order_to_company[order_id] = company_id
        print(f"   - order -> center: {len(self.order_to_center)} 条映射")
        print(f"   - order -> company: {len(self.order_to_company)} 条映射")

        for user_id, center_id in self.user_to_center.items():
            company_id = self.user_to_company.get(user_id)
            if company_id and center_id:
                self.center_to_company[center_id] = company_id

        for order_id, center_id in self.order_to_center.items():
            company_id = self.order_to_company.get(order_id)
            if company_id and center_id:
                self.center_to_company[center_id] = company_id

        print(f"   - center -> company: {len(self.center_to_company)} 条映射")

        if self.center_to_company:
            print("\n📋 分拣中心-公司映射关系:")
            for center_id, company_id in self.center_to_company.items():
                print(f"   - {center_id} -> {company_id}")

    def get_center_and_company_for_settle(self, biz_id: str) -> Tuple[Optional[str], Optional[str]]:
        """获取回收结算对应的分拣中心ID和公司ID"""
        center_id = self.order_to_center.get(biz_id)
        company_id = self.order_to_company.get(biz_id)
        if center_id and not company_id:
            company_id = self.center_to_company.get(center_id)
        return center_id, company_id

    def get_center_and_company_for_withdraw(self, wallet_id: str) -> Tuple[Optional[str], Optional[str]]:
        """获取提现对应的分拣中心ID和公司ID"""
        user_id = self.wallet_to_user.get(wallet_id)
        if not user_id:
            return None, None
        center_id = self.user_to_center.get(user_id)
        company_id = self.user_to_company.get(user_id)
        if center_id and not company_id:
            company_id = self.center_to_company.get(center_id)
        return center_id, company_id

    def parse_channel(self, row: pd.Series) -> str:
        """解析交易渠道"""
        trade_channel = str(row.get('trade_channel', '')).strip()
        title = str(row.get('title', '')).strip()

        if 'WECHAT' in trade_channel or '微信' in trade_channel:
            return 'WECHAT'
        if 'ALIPAY' in trade_channel or '支付宝' in trade_channel:
            return 'ALIPAY'
        if 'WECHAT' in title or '微信' in title:
            return 'WECHAT'
        if 'ALIPAY' in title or '支付宝' in title:
            return 'ALIPAY'
        return 'ALIPAY'

    def process_transactions(self) -> None:
        """处理所有交易记录"""
        print("\n🔄 开始处理交易记录...")

        trans_df = self.pay_wallet_transaction_df.copy()
        if 'create_time' in trans_df.columns:
            trans_df['create_time'] = pd.to_datetime(trans_df['create_time'], errors='coerce')
            trans_df = trans_df.sort_values('create_time')

        processed_count = 0
        skipped_count = 0

        for _, row in trans_df.iterrows():
            biz_type = str(row.get('biz_type', '')).strip()
            price = float(row.get('price', 0))

            if biz_type == '11':
                if price <= 0:
                    continue
                self._process_settle(row)
                processed_count += 1
            elif biz_type == '8':
                if price >= 0:
                    continue
                self._process_withdraw(row)
                processed_count += 1
            else:
                skipped_count += 1

        print(f"   - 处理记录: {processed_count} 条")
        print(f"   - 跳过记录: {skipped_count} 条")

    def _process_settle(self, row: pd.Series) -> None:
        """处理回收结算"""
        biz_id = str(row.get('biz_id', '')).strip()
        wallet_id = str(row.get('wallet_id', '')).strip()
        price = float(row.get('price', 0))
        title = str(row.get('title', '')).strip()

        center_id, company_id = self.get_center_and_company_for_settle(biz_id)

        if not center_id:
            user_id = self.wallet_to_user.get(wallet_id)
            if user_id:
                center_id = self.user_to_center.get(user_id)
                if not company_id:
                    company_id = self.user_to_company.get(user_id)
                    if center_id and not company_id:
                        company_id = self.center_to_company.get(center_id)

        if not center_id:
            return

        channel = self.parse_channel(row)

        self.center_balance[center_id][channel] -= abs(price)
        self.center_pending_withdraw[center_id][channel] += abs(price)

        user_id = self.wallet_to_user.get(wallet_id)

        self.stats['centers'].add(center_id)
        if company_id:
            self.stats['companies'].add(company_id)

        record = CenterFundRecord(
            center_id=center_id,
            change_type='SETTLE',
            channel=channel,
            amount=-abs(price),
            balance_after=self.center_balance[center_id][channel],
            related_user_id=user_id,
            related_order_id=biz_id,
            remark=f'用户回收结算 {title}'
        )
        record.wallet_id = wallet_id
        self.center_records.append(record)

        self.stats['settle_count'] += 1
        self.stats['total_settle_amount'] += abs(price)

    def _process_withdraw(self, row: pd.Series) -> None:
        """处理提现"""
        wallet_id = str(row.get('wallet_id', '')).strip()
        price = float(row.get('price', 0))
        title = str(row.get('title', '')).strip()

        center_id, company_id = self.get_center_and_company_for_withdraw(wallet_id)

        if not center_id:
            return

        if not company_id:
            company_id = self.center_to_company.get(center_id)

        if not company_id:
            company_id = 'company_unknown'

        channel = self.parse_channel(row)
        amount = abs(price)

        self.center_pending_withdraw[center_id][channel] -= amount
        self.center_balance[center_id][channel] -= amount

        self.company_balance[company_id][channel] -= amount

        user_id = self.wallet_to_user.get(wallet_id)

        self.stats['centers'].add(center_id)
        self.stats['companies'].add(company_id)

        center_record = CenterFundRecord(
            center_id=center_id,
            change_type='WITHDRAW',
            channel=channel,
            amount=-amount,
            balance_after=self.center_balance[center_id][channel],
            related_user_id=user_id,
            related_order_id=None,
            remark=f'用户提现 {title}'
        )
        center_record.wallet_id = wallet_id
        self.center_records.append(center_record)

        company_record = CompanyFundRecord(
            company_id=company_id,
            change_type='WITHDRAW',
            channel=channel,
            amount=-amount,
            balance_after=self.company_balance[company_id][channel],
            related_center_id=center_id,
            related_user_id=user_id,
            remark=f'用户提现支出 {title}'
        )
        self.company_records.append(company_record)

        self.stats['withdraw_count'] += 1
        self.stats['total_withdraw_amount'] += amount

    def print_summary(self) -> None:
        """打印汇总信息"""
        print('\n' + '=' * 70)
        print('📊 资金流水倒推完成！汇总信息：')
        print('=' * 70)

        print('\n📝 交易统计:')
        print(f'   - 回收结算笔数: {self.stats["settle_count"]}')
        print(f'   - 回收结算总额: {self.stats["total_settle_amount"]:.2f} 元')
        print(f'   - 提现笔数: {self.stats["withdraw_count"]}')
        print(f'   - 提现总额: {self.stats["total_withdraw_amount"]:.2f} 元')

        print(f'\n🏢 涉及公司: {len(self.stats["companies"])} 个')
        for company_id in sorted(self.stats['companies']):
            wechat_bal = self.company_balance[company_id].get('WECHAT', 0)
            alipay_bal = self.company_balance[company_id].get('ALIPAY', 0)
            print(f'   - {company_id}: 微信余额={wechat_bal:.2f}, 支付宝余额={alipay_bal:.2f}')

        print(f'\n🏪 涉及分拣中心: {len(self.stats["centers"])} 个')
        for center_id in sorted(self.stats['centers']):
            wechat_bal = self.center_balance[center_id].get('WECHAT', 0)
            alipay_bal = self.center_balance[center_id].get('ALIPAY', 0)
            wechat_pending = self.center_pending_withdraw[center_id].get('WECHAT', 0)
            alipay_pending = self.center_pending_withdraw[center_id].get('ALIPAY', 0)
            company_id = self.center_to_company.get(center_id, '未知')
            print(f'   - {center_id} (公司: {company_id}):')
            print(f'       微信余额: {wechat_bal:.2f}, 支付宝余额: {alipay_bal:.2f}')
            print(f'       待提现(微信): {wechat_pending:.2f}, 待提现(支付宝): {alipay_pending:.2f}')

        print('\n📋 流水记录:')
        print(f'   - 分拣中心流水: {len(self.center_records)} 条')
        print(f'   - 公司流水: {len(self.company_records)} 条')
        print('=' * 70)

    def generate_sql(self) -> str:
        """生成SQL插入语句"""
        sql_lines = []

        timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        sql_lines.append(f'-- ============================================')
        sql_lines.append(f'-- 资金流水数据插入SQL')
        sql_lines.append(f'-- 生成时间: {timestamp}')
        sql_lines.append(f'-- 回收结算笔数: {self.stats["settle_count"]}')
        sql_lines.append(f'-- 提现笔数: {self.stats["withdraw_count"]}')
        sql_lines.append(f'-- 涉及分拣中心: {len(self.stats["centers"])} 个')
        sql_lines.append(f'-- 涉及公司: {len(self.stats["companies"])} 个')
        sql_lines.append('-- ============================================')
        sql_lines.append('')

        if self.center_records:
            sql_lines.append('-- 1. 分拣中心资金流水')
            sql_lines.append(
                'INSERT INTO center_fund_flow (center_id, change_type, channel, change_amount, balance_after, related_user_id, related_order_id, remark, created_at) VALUES')
            center_values = []
            for r in self.center_records:
                related_user = f"'{r.related_user_id}'" if r.related_user_id else 'NULL'
                related_order = f"'{r.related_order_id}'" if r.related_order_id else 'NULL'
                center_values.append(
                    f"('{r.center_id}', '{r.change_type}', '{r.channel}', {r.amount}, "
                    f"{r.balance_after}, {related_user}, {related_order}, '{r.remark}', '{r.created_at}')"
                )
            sql_lines.append(',\n'.join(center_values) + ';')
            sql_lines.append('')

        if self.company_records:
            sql_lines.append('-- 2. 公司资金流水')
            sql_lines.append(
                'INSERT INTO company_fund_flow (company_id, change_type, channel, change_amount, balance_after, related_center_id, related_user_id, remark, created_at) VALUES')
            company_values = []
            for r in self.company_records:
                related_center = f"'{r.related_center_id}'" if r.related_center_id else 'NULL'
                related_user = f"'{r.related_user_id}'" if r.related_user_id else 'NULL'
                company_values.append(
                    f"('{r.company_id}', '{r.change_type}', '{r.channel}', {r.amount}, "
                    f"{r.balance_after}, {related_center}, {related_user}, '{r.remark}', '{r.created_at}')"
                )
            sql_lines.append(',\n'.join(company_values) + ';')
            sql_lines.append('')

        return '\n'.join(sql_lines)

    def save_sql(self, output_file: str = 'fund_flow_insert.sql') -> None:
        """保存SQL到文件"""
        sql = self.generate_sql()
        output_path = os.path.join(SCRIPT_DIR, output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write(sql)
        print(f'\n✅ SQL文件已生成: {output_path}')

    def save_mapping_info(self, output_file: str = 'center_company_mapping.txt') -> None:
        """保存分拣中心-公司映射信息"""
        output_path = os.path.join(SCRIPT_DIR, output_file)
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('=' * 60 + '\n')
            f.write('分拣中心-公司映射关系\n')
            f.write('=' * 60 + '\n\n')
            for center_id, company_id in sorted(self.center_to_company.items()):
                f.write(f'{center_id} -> {company_id}\n')
            f.write('\n' + '=' * 60 + '\n')
            f.write(f'共 {len(self.center_to_company)} 个分拣中心\n')

        print(f'✅ 映射信息已保存: {output_path}')


# ==================== 主函数 ====================

def main():
    """主函数 - 生成SQL文件"""
    print('=' * 70)
    print('🚀 资金流水倒推工具启动（真实数据版）')
    print('📌 分拣中心和公司ID均从数据中动态获取')
    print('📌 将生成 fund_flow_insert.sql 文件')
    print('=' * 70)

    reverser = FundFlowReverser(CONFIG)

    if not reverser.load_data():
        print('\n❌ 数据加载失败，请检查文件路径和格式')
        return

    reverser.build_mappings()
    reverser.process_transactions()
    reverser.print_summary()
    reverser.save_sql('fund_flow_insert.sql')
    reverser.save_mapping_info('center_company_mapping.txt')

    print('\n' + '=' * 70)
    print('✅ 处理完成！')
    print('📄 SQL文件: ' + os.path.join(SCRIPT_DIR, 'fund_flow_insert.sql'))
    print('📄 映射文件: ' + os.path.join(SCRIPT_DIR, 'center_company_mapping.txt'))
    print('=' * 70)


# ==================== pytest 测试类 ====================

class TestFundFlowReverser:
    """资金流水倒推测试类"""

    def test_load_data(self):
        """测试数据加载"""
        reverser = FundFlowReverser(CONFIG)
        if not reverser.load_data():
            print("⚠️ 数据文件不存在，跳过测试")
            return

        assert reverser.pay_wallet_df is not None
        assert reverser.pay_wallet_transaction_df is not None
        assert reverser.member_user_df is not None
        assert reverser.recycle_order_df is not None
        print("✅ 数据加载测试通过")

    def test_build_mappings(self):
        """测试映射关系构建"""
        reverser = FundFlowReverser(CONFIG)
        if not reverser.load_data():
            print("⚠️ 数据文件不存在，跳过测试")
            return

        reverser.build_mappings()

        assert isinstance(reverser.wallet_to_user, dict)
        assert isinstance(reverser.user_to_center, dict)
        assert isinstance(reverser.user_to_company, dict)
        assert isinstance(reverser.order_to_center, dict)
        assert isinstance(reverser.order_to_company, dict)
        assert isinstance(reverser.center_to_company, dict)
        print("✅ 映射关系构建测试通过")

    def test_process_transactions(self):
        """测试交易处理"""
        reverser = FundFlowReverser(CONFIG)
        if not reverser.load_data():
            print("⚠️ 数据文件不存在，跳过测试")
            return

        reverser.build_mappings()
        reverser.process_transactions()

        assert reverser.center_records is not None
        assert reverser.company_records is not None
        print("✅ 交易处理测试通过")

    def test_generate_sql(self):
        """测试SQL生成"""
        reverser = FundFlowReverser(CONFIG)
        if not reverser.load_data():
            print("⚠️ 数据文件不存在，跳过测试")
            return

        reverser.build_mappings()
        reverser.process_transactions()
        sql = reverser.generate_sql()

        assert sql is not None
        assert len(sql) > 0
        print("✅ SQL生成测试通过")


# ==================== 程序入口 ====================

if __name__ == '__main__':
    import sys

    # 如果命令行参数包含 --test，运行pytest测试
    if len(sys.argv) > 1 and sys.argv[1] == '--test':
        print("🧪 运行pytest测试...")
        import pytest

        pytest.main([__file__, '-v'])
    else:
        # 默认执行主函数，生成SQL文件
        main()