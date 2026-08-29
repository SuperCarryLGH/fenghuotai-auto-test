-- ============================================
-- 资金初始化 SQL - 浙江恒逸 (2026-07-25 10:18)
-- ============================================

BEGIN;

-- pay_fund UPDATE
UPDATE pay_fund SET total_fund=2000000, wechat_fund=1000000, alipay_fund=1000000, updater=0, update_time=NOW() WHERE fund_type=20 AND org_id=2067090140163862530;

COMMIT;