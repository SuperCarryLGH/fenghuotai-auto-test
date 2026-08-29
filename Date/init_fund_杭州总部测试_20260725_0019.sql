-- ============================================
-- 资金初始化 SQL - 杭州总部测试 (2026-07-25 00:19)
-- ============================================

BEGIN;

-- 回收结算 wallet_tx
INSERT INTO pay_wallet_transaction (wallet_id, biz_type, biz_id, title, price, balance, creator, updater, create_time, update_time, deleted, tenant_id) VALUES (2066497131584860162, 11, '2071957903323652097', '回收结算', -30, 9529581, 0, 0, '2026-06-30 22:03:56', '2026-06-30 22:03:56', 0, 1);
-- 回收结算 wallet_tx
INSERT INTO pay_wallet_transaction (wallet_id, biz_type, biz_id, title, price, balance, creator, updater, create_time, update_time, deleted, tenant_id) VALUES (2066497131584860162, 11, '2071958721516945409', '回收结算', -30, 9529551, 0, 0, '2026-06-30 22:07:10', '2026-06-30 22:07:10', 0, 1);
-- 回收结算 wallet_tx
INSERT INTO pay_wallet_transaction (wallet_id, biz_type, biz_id, title, price, balance, creator, updater, create_time, update_time, deleted, tenant_id) VALUES (2066497131584860162, 11, '2071963920809312258', '回收结算', -30, 9529521, 0, 0, '2026-06-30 22:27:51', '2026-06-30 22:27:51', 0, 1);
-- 回收结算 wallet_tx
INSERT INTO pay_wallet_transaction (wallet_id, biz_type, biz_id, title, price, balance, creator, updater, create_time, update_time, deleted, tenant_id) VALUES (2066497131584860162, 11, '2071971859387752450', '回收结算', -100, 9529421, 0, 0, '2026-06-30 22:59:23', '2026-06-30 22:59:23', 0, 1);

COMMIT;