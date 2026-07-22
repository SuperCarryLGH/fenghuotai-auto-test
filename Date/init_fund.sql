-- ============================================
-- 资金初始化 SQL (2026-07-14 09:16)
-- ============================================

BEGIN;

-- === 公司: 公司3 (orgId=3) ===

INSERT INTO pay_fund (fund_type, org_id, company_id, total_fund, wechat_fund, alipay_fund, allocable_fund, allocated_fund, company_name, org_name, fund_purpose, tenant_id, creator, create_time, update_time) VALUES (
  10, 3, '', 164104, 164104, 0, 0, 164104, '公司3', '公司3', 2, 1, 'init_script', NOW(), NOW());

INSERT INTO pay_fund (fund_type, org_id, company_id, total_fund, wechat_fund, alipay_fund, allocable_fund, allocated_fund, company_name, org_name, fund_purpose, tenant_id, creator, create_time, update_time) VALUES (
  10, 3, '', -1890, -1390, -500, NULL, NULL, '公司3', '杭州总部测试', 2, 1, 'init_script', NOW(), NOW());

INSERT INTO pay_fund (fund_type, org_id, company_id, total_fund, wechat_fund, alipay_fund, allocable_fund, allocated_fund, company_name, org_name, fund_purpose, tenant_id, creator, create_time, update_time) VALUES (
  10, 2069365345938698241, '', -88209, -100, -88109, NULL, NULL, '公司3', '温州恒逸分拣中心', 2, 1, 'init_script', NOW(), NOW());

INSERT INTO pay_fund (fund_type, org_id, company_id, total_fund, wechat_fund, alipay_fund, allocable_fund, allocated_fund, company_name, org_name, fund_purpose, tenant_id, creator, create_time, update_time) VALUES (
  10, 2071977701136384001, '', -5085, 0, -5085, NULL, NULL, '公司3', '常州分拣中心', 2, 1, 'init_script', NOW(), NOW());

-- 常州分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202605191312291', 2071977701136384001, 50, 0, 100, 1000, 900, 1, '2026-05-19 13:12:29' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 常州分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202605241408461', 2071977701136384001, 50, 0, 100, 1418, 1318, 1, '2026-05-24 14:08:47' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202606091713261', 2069365345938698241, 50, 0, 418, 419, 1, 1, '2026-06-09 17:13:26' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202606221809031', 2069365345938698241, 50, 0, 1623, 1624, 1, 1, '2026-06-22 18:09:04' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202606230659521', 2069365345938698241, 50, 0, 876, 876, 0, 1, '2026-06-23 06:59:53' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202606291534561', 2069365345938698241, 50, 0, 357, 357, 0, 1, '2026-06-29 15:34:56' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 杭州总部测试 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202606302132411', 3, 40, 0, 210000, 0, 210000, 1, '2026-06-30 21:32:41' FROM pay_fund WHERE fund_type=10 AND org_id=3 LIMIT 1;
-- 杭州总部测试 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202606302203551', 3, 40, 0, 30, 210000, 210030, 1, '2026-06-30 22:03:56' FROM pay_fund WHERE fund_type=10 AND org_id=3 LIMIT 1;
-- 杭州总部测试 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202606302207101', 3, 40, 0, 30, 210030, 210060, 1, '2026-06-30 22:07:10' FROM pay_fund WHERE fund_type=10 AND org_id=3 LIMIT 1;
-- 杭州总部测试 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202606302207401', 3, 40, 0, 50000, 210060, 260060, 1, '2026-06-30 22:07:40' FROM pay_fund WHERE fund_type=10 AND org_id=3 LIMIT 1;
-- 杭州总部测试 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202606302216441', 3, 40, 0, 250000, 260060, 510060, 1, '2026-06-30 22:16:45' FROM pay_fund WHERE fund_type=10 AND org_id=3 LIMIT 1;
-- 杭州总部测试 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202606302227311', 3, 40, 0, 30000, 510060, 540060, 1, '2026-06-30 22:27:31' FROM pay_fund WHERE fund_type=10 AND org_id=3 LIMIT 1;
-- 杭州总部测试 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202606302227511', 3, 40, 0, 30, 540060, 540090, 1, '2026-06-30 22:27:51' FROM pay_fund WHERE fund_type=10 AND org_id=3 LIMIT 1;
-- 杭州总部测试 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202606302233011', 3, 40, 0, 30000, 540090, 570090, 1, '2026-06-30 22:33:02' FROM pay_fund WHERE fund_type=10 AND org_id=3 LIMIT 1;
-- 常州分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202606302237201', 2071977701136384001, 50, 0, 100, 3418, 3318, 1, '2026-06-30 22:37:20' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 常州分拣中心 bt=9
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202606302237211', 2071977701136384001, 50, 0, 100, 3318, 3418, 1, '2026-06-30 22:37:21' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 杭州总部测试 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202606302259221', 3, 40, 0, 100, 0, 100, 1, '2026-06-30 22:59:23' FROM pay_fund WHERE fund_type=10 AND org_id=3 LIMIT 1;
-- 常州分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202606302301321', 2071977701136384001, 50, 0, 100, 3418, 3318, 1, '2026-06-30 23:01:33' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 杭州总部测试 bt=9
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202606302336472', 3, 50, 0, 100, 569990, 570090, 1, '2026-06-30 23:36:47' FROM pay_fund WHERE fund_type=10 AND org_id=3 LIMIT 1;
-- 杭州总部测试 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202606302336471', 3, 50, 0, 100, 570090, 569990, 1, '2026-06-30 23:36:47' FROM pay_fund WHERE fund_type=10 AND org_id=3 LIMIT 1;
-- 杭州总部测试 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202606302338311', 3, 50, 0, 100, 570090, 569990, 1, '2026-06-30 23:38:32' FROM pay_fund WHERE fund_type=10 AND org_id=3 LIMIT 1;
-- 杭州总部测试 bt=9
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202606302338321', 3, 50, 0, 100, 569990, 570090, 1, '2026-06-30 23:38:32' FROM pay_fund WHERE fund_type=10 AND org_id=3 LIMIT 1;
-- 杭州总部测试 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202606302346401', 3, 50, 0, 100, 570090, 569990, 1, '2026-06-30 23:46:41' FROM pay_fund WHERE fund_type=10 AND org_id=3 LIMIT 1;
-- 杭州总部测试 bt=9
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202606302346411', 3, 50, 0, 100, 569990, 570090, 1, '2026-06-30 23:46:41' FROM pay_fund WHERE fund_type=10 AND org_id=3 LIMIT 1;
-- 杭州总部测试 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607010000521', 3, 40, 0, 70, 570090, 570160, 1, '2026-07-01 00:00:52' FROM pay_fund WHERE fund_type=10 AND org_id=3 LIMIT 1;
-- 杭州总部测试 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607010009281', 3, 40, 0, 70, 570160, 570230, 1, '2026-07-01 00:09:29' FROM pay_fund WHERE fund_type=10 AND org_id=3 LIMIT 1;
-- 常州分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607010051261', 2071977701136384001, 50, 0, 100, 3318, 3218, 1, '2026-07-01 00:51:27' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 常州分拣中心 bt=9
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607010051271', 2071977701136384001, 50, 0, 100, 3218, 3318, 1, '2026-07-01 00:51:27' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 常州分拣中心 bt=9
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607010053372', 2071977701136384001, 50, 0, 100, 3218, 3318, 1, '2026-07-01 00:53:37' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 常州分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607010053371', 2071977701136384001, 50, 0, 100, 3318, 3218, 1, '2026-07-01 00:53:37' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 常州分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607010055241', 2071977701136384001, 50, 0, 100, 3318, 3218, 1, '2026-07-01 00:55:24' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 常州分拣中心 bt=9
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607010055242', 2071977701136384001, 50, 0, 100, 3218, 3318, 1, '2026-07-01 00:55:25' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 常州分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607010107091', 2071977701136384001, 50, 0, 100, 3318, 3218, 1, '2026-07-01 01:07:09' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 常州分拣中心 bt=9
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607010107101', 2071977701136384001, 50, 0, 100, 3218, 3318, 1, '2026-07-01 01:07:10' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607010254011', 2069365345938698241, 40, 0, 70, 0, 70, 1, '2026-07-01 02:54:02' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607010710101', 2069365345938698241, 40, 0, 70, 70, 140, 1, '2026-07-01 07:10:11' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607010713081', 2069365345938698241, 40, 0, 70, 140, 210, 1, '2026-07-01 07:13:08' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607010719511', 2069365345938698241, 50, 0, 100, 210, 110, 1, '2026-07-01 07:19:52' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=9
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607010719521', 2069365345938698241, 50, 0, 100, 110, 210, 1, '2026-07-01 07:19:53' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607010722001', 2069365345938698241, 50, 0, 100, 210, 110, 1, '2026-07-01 07:22:00' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=9
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607010722011', 2069365345938698241, 50, 0, 100, 110, 210, 1, '2026-07-01 07:22:01' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607010729331', 2069365345938698241, 50, 0, 100, 210, 110, 1, '2026-07-01 07:29:34' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=9
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607010729341', 2069365345938698241, 50, 0, 100, 110, 210, 1, '2026-07-01 07:29:34' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607010736161', 2069365345938698241, 50, 0, 100, 210, 110, 1, '2026-07-01 07:36:17' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=9
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607010736171', 2069365345938698241, 50, 0, 100, 110, 210, 1, '2026-07-01 07:36:18' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607010743081', 2069365345938698241, 50, 0, 100, 210, 110, 1, '2026-07-01 07:43:08' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=9
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607010743091', 2069365345938698241, 50, 0, 100, 110, 210, 1, '2026-07-01 07:43:09' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607010752101', 2069365345938698241, 50, 0, 100, 210, 110, 1, '2026-07-01 07:52:11' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=9
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607010752111', 2069365345938698241, 50, 0, 100, 110, 210, 1, '2026-07-01 07:52:12' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607010756451', 2069365345938698241, 50, 0, 100, 210, 110, 1, '2026-07-01 07:56:45' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=9
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607010756461', 2069365345938698241, 50, 0, 100, 110, 210, 1, '2026-07-01 07:56:47' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607010805381', 2069365345938698241, 50, 0, 100, 210, 110, 1, '2026-07-01 08:05:39' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607011258441', 2069365345938698241, 40, 0, 392, 700, 1092, 1, '2026-07-01 12:58:45' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607011354291', 2069365345938698241, 40, 0, 2100, 0, 2100, 1, '2026-07-01 13:54:29' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607011618221', 2069365345938698241, 50, 0, 2100, 2100, 0, 1, '2026-07-01 16:18:22' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607011738381', 2069365345938698241, 40, 0, 1134, 0, 1134, 1, '2026-07-01 17:38:38' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 杭州总部测试 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607011848431', 3, 50, 0, 100, 570230, 570130, 1, '2026-07-01 18:48:44' FROM pay_fund WHERE fund_type=10 AND org_id=3 LIMIT 1;
-- 杭州总部测试 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607011859581', 3, 50, 0, 100, 570130, 570030, 1, '2026-07-01 18:59:58' FROM pay_fund WHERE fund_type=10 AND org_id=3 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607011901361', 2069365345938698241, 40, 0, 1190, 0, 1190, 1, '2026-07-01 19:01:36' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607011927201', 2069365345938698241, 40, 0, 840, 0, 840, 1, '2026-07-01 19:27:21' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607011927411', 2069365345938698241, 40, 0, 756, 0, 756, 1, '2026-07-01 19:27:41' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607011941341', 2069365345938698241, 40, 0, 392, 0, 392, 1, '2026-07-01 19:41:34' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607012020051', 2069365345938698241, 40, 0, 644, 0, 644, 1, '2026-07-01 20:20:05' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607012214521', 2069365345938698241, 50, 0, 1190, 1190, 0, 1, '2026-07-01 22:14:53' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607021335561', 2069365345938698241, 50, 0, 840, 840, 0, 1, '2026-07-02 13:35:57' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607021343591', 2069365345938698241, 50, 0, 1134, 1134, 0, 1, '2026-07-02 13:44:00' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607021344191', 2069365345938698241, 40, 0, 357, 0, 357, 1, '2026-07-02 13:44:19' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607021351221', 2069365345938698241, 40, 0, 560, 2100, 2660, 1, '2026-07-02 13:51:23' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607021357341', 2069365345938698241, 50, 0, 357, 357, 0, 1, '2026-07-02 13:57:34' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607021618281', 2069365345938698241, 40, 0, 609, 0, 609, 1, '2026-07-02 16:18:29' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607021705541', 2069365345938698241, 40, 0, 459, 0, 459, 1, '2026-07-02 17:05:55' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607021722551', 2069365345938698241, 40, 0, 1001, 0, 1001, 1, '2026-07-02 17:22:55' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607021734361', 2069365345938698241, 40, 0, 4200, 0, 4200, 1, '2026-07-02 17:34:36' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607021741581', 2069365345938698241, 40, 0, 1120, 0, 1120, 1, '2026-07-02 17:41:58' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607021750491', 2069365345938698241, 40, 0, 767, 0, 767, 1, '2026-07-02 17:50:49' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607021756231', 2069365345938698241, 40, 0, 763, 0, 763, 1, '2026-07-02 17:56:24' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607021818191', 2069365345938698241, 40, 0, 1785, 0, 1785, 1, '2026-07-02 18:18:19' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607021844401', 2069365345938698241, 40, 0, 560, 0, 560, 1, '2026-07-02 18:44:40' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607021859281', 2069365345938698241, 40, 0, 735, 0, 735, 1, '2026-07-02 18:59:28' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607021928101', 2069365345938698241, 40, 0, 700, 0, 700, 1, '2026-07-02 19:28:11' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607021949481', 2069365345938698241, 40, 0, 560, 0, 560, 1, '2026-07-02 19:49:48' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607021954551', 2069365345938698241, 40, 0, 700, 0, 700, 1, '2026-07-02 19:54:55' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607021957001', 2069365345938698241, 40, 0, 630, 525, 1155, 1, '2026-07-02 19:57:01' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607022142001', 2069365345938698241, 50, 0, 735, 735, 0, 1, '2026-07-02 21:42:00' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607022236471', 2069365345938698241, 50, 0, 700, 700, 0, 1, '2026-07-02 22:36:48' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607030929401', 2069365345938698241, 40, 0, 742, 0, 742, 1, '2026-07-03 09:29:40' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607030948111', 2069365345938698241, 50, 0, 742, 742, 0, 1, '2026-07-03 09:48:12' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607031046021', 2069365345938698241, 50, 0, 1784, 1785, 1, 1, '2026-07-03 10:46:03' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607031245161', 2069365345938698241, 40, 0, 630, 0, 630, 1, '2026-07-03 12:45:16' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607031323211', 2069365345938698241, 40, 0, 424, 0, 424, 1, '2026-07-03 13:23:21' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607031341111', 2069365345938698241, 40, 0, 413, 0, 413, 1, '2026-07-03 13:41:11' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607031353061', 2069365345938698241, 40, 0, 721, 0, 721, 1, '2026-07-03 13:53:06' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607031428011', 2069365345938698241, 40, 0, 1225, 0, 1225, 1, '2026-07-03 14:28:02' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607031453561', 2069365345938698241, 40, 0, 1365, 0, 1365, 1, '2026-07-03 14:53:57' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607031616161', 2069365345938698241, 40, 0, 1386, 0, 1386, 1, '2026-07-03 16:16:16' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607031627211', 2069365345938698241, 40, 0, 567, 0, 567, 1, '2026-07-03 16:27:21' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607031632411', 2069365345938698241, 40, 0, 490, 1, 491, 1, '2026-07-03 16:32:42' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607031647161', 2069365345938698241, 50, 0, 4200, 4200, 0, 1, '2026-07-03 16:47:17' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607031718161', 2069365345938698241, 40, 0, 641, 910, 1551, 1, '2026-07-03 17:18:16' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607031803011', 2069365345938698241, 40, 0, 602, 0, 602, 1, '2026-07-03 18:03:01' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607031807111', 2069365345938698241, 40, 0, 945, 0, 945, 1, '2026-07-03 18:07:12' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607031831111', 2069365345938698241, 40, 0, 1470, 0, 1470, 1, '2026-07-03 18:31:11' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607031842061', 2069365345938698241, 50, 0, 630, 630, 0, 1, '2026-07-03 18:42:06' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607032035311', 2069365345938698241, 40, 0, 1141, 0, 1141, 1, '2026-07-03 20:35:31' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607032054081', 2069365345938698241, 50, 0, 560, 560, 0, 1, '2026-07-03 20:54:09' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607032207021', 2069365345938698241, 50, 0, 100, 110, 10, 1, '2026-07-03 22:07:02' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607040723051', 2069365345938698241, 50, 0, 1100, 1120, 20, 1, '2026-07-04 07:23:06' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607040935371', 2069365345938698241, 40, 0, 777, 0, 777, 1, '2026-07-04 09:35:37' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041025311', 2069365345938698241, 40, 0, 490, 0, 490, 1, '2026-07-04 10:25:31' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041101171', 2069365345938698241, 40, 0, 392, 0, 392, 1, '2026-07-04 11:01:17' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041129361', 2069365345938698241, 40, 0, 1091, 3500, 4591, 1, '2026-07-04 11:29:36' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041200311', 2069365345938698241, 40, 0, 1050, 0, 1050, 1, '2026-07-04 12:00:31' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041348061', 2069365345938698241, 40, 0, 700, 0, 700, 1, '2026-07-04 13:48:06' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041354151', 2069365345938698241, 40, 0, 455, 0, 455, 1, '2026-07-04 13:54:16' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041400061', 2069365345938698241, 40, 0, 620, 4591, 5211, 1, '2026-07-04 14:00:07' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041401201', 2069365345938698241, 40, 0, 1400, 0, 1400, 1, '2026-07-04 14:01:21' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041436211', 2069365345938698241, 40, 0, 532, 0, 532, 1, '2026-07-04 14:36:22' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041437411', 2069365345938698241, 40, 0, 1050, 0, 1050, 1, '2026-07-04 14:37:42' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041455361', 2069365345938698241, 40, 0, 630, 1029, 1659, 1, '2026-07-04 14:55:36' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041511151', 2069365345938698241, 40, 0, 1190, 0, 1190, 1, '2026-07-04 15:11:16' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041551121', 2069365345938698241, 40, 0, 490, 0, 490, 1, '2026-07-04 15:51:12' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041608411', 2069365345938698241, 40, 0, 616, 567, 1183, 1, '2026-07-04 16:08:41' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041613161', 2069365345938698241, 40, 0, 1029, 0, 1029, 1, '2026-07-04 16:13:16' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041652261', 2069365345938698241, 40, 0, 455, 0, 455, 1, '2026-07-04 16:52:27' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041718011', 2069365345938698241, 40, 0, 665, 0, 665, 1, '2026-07-04 17:18:02' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041735101', 2069365345938698241, 40, 0, 805, 0, 805, 1, '2026-07-04 17:35:11' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041821161', 2069365345938698241, 40, 0, 2345, 0, 2345, 1, '2026-07-04 18:21:17' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041824161', 2069365345938698241, 40, 0, 1106, 0, 1106, 1, '2026-07-04 18:24:16' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041839171', 2069365345938698241, 40, 0, 1120, 0, 1120, 1, '2026-07-04 18:39:17' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041841011', 2069365345938698241, 40, 0, 1106, 0, 1106, 1, '2026-07-04 18:41:01' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041842301', 2069365345938698241, 50, 0, 721, 721, 0, 1, '2026-07-04 18:42:30' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041848361', 2069365345938698241, 40, 0, 1274, 0, 1274, 1, '2026-07-04 18:48:36' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041856461', 2069365345938698241, 40, 0, 2240, 0, 2240, 1, '2026-07-04 18:56:47' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041856541', 2069365345938698241, 50, 0, 532, 532, 0, 1, '2026-07-04 18:56:55' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041858461', 2069365345938698241, 40, 0, 700, 1061, 1761, 1, '2026-07-04 18:58:47' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041859011', 2069365345938698241, 40, 0, 609, 0, 609, 1, '2026-07-04 18:59:01' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041911011', 2069365345938698241, 40, 0, 357, 0, 357, 1, '2026-07-04 19:11:01' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041926261', 2069365345938698241, 40, 0, 476, 0, 476, 1, '2026-07-04 19:26:27' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041927351', 2069365345938698241, 40, 0, 784, 0, 784, 1, '2026-07-04 19:27:36' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041944411', 2069365345938698241, 40, 0, 777, 0, 777, 1, '2026-07-04 19:44:42' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607041947111', 2069365345938698241, 50, 0, 5211, 5211, 0, 1, '2026-07-04 19:47:12' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607042006301', 2069365345938698241, 40, 0, 910, 0, 910, 1, '2026-07-04 20:06:31' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607042014161', 2069365345938698241, 40, 0, 1407, 0, 1407, 1, '2026-07-04 20:14:16' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607042109441', 2069365345938698241, 50, 0, 1183, 1183, 0, 1, '2026-07-04 21:09:44' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607042133351', 2069365345938698241, 50, 0, 1100, 1120, 20, 1, '2026-07-04 21:33:36' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607042147251', 2069365345938698241, 40, 0, 4200, 0, 4200, 1, '2026-07-04 21:47:26' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607042332461', 2069365345938698241, 50, 0, 1106, 1106, 0, 1, '2026-07-04 23:32:47' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607050940531', 2069365345938698241, 50, 0, 476, 476, 0, 1, '2026-07-05 09:40:54' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607051000161', 2069365345938698241, 40, 0, 389, 0, 389, 1, '2026-07-05 10:00:16' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607051024071', 2069365345938698241, 40, 0, 459, 0, 459, 1, '2026-07-05 10:24:07' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607051054451', 2069365345938698241, 40, 0, 3192, 0, 3192, 1, '2026-07-05 10:54:46' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607051235001', 2069365345938698241, 40, 0, 2482, 0, 2482, 1, '2026-07-05 12:35:01' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607051240501', 2069365345938698241, 40, 0, 700, 0, 700, 1, '2026-07-05 12:40:51' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607051241251', 2069365345938698241, 40, 0, 791, 0, 791, 1, '2026-07-05 12:41:26' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607051323101', 2069365345938698241, 40, 0, 525, 0, 525, 1, '2026-07-05 13:23:11' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607051326551', 2069365345938698241, 40, 0, 980, 0, 980, 1, '2026-07-05 13:26:56' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607051400111', 2069365345938698241, 40, 0, 1733, 0, 1733, 1, '2026-07-05 14:00:12' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607051403551', 2069365345938698241, 40, 0, 1295, 0, 1295, 1, '2026-07-05 14:03:56' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607051428251', 2069365345938698241, 40, 0, 2100, 0, 2100, 1, '2026-07-05 14:28:26' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607051439261', 2069365345938698241, 40, 0, 770, 0, 770, 1, '2026-07-05 14:39:26' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607051543351', 2069365345938698241, 40, 0, 623, 0, 623, 1, '2026-07-05 15:43:36' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607051551511', 2069365345938698241, 40, 0, 980, 0, 980, 1, '2026-07-05 15:51:51' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607051559551', 2069365345938698241, 40, 0, 921, 0, 921, 1, '2026-07-05 15:59:56' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607051604501', 2069365345938698241, 40, 0, 882, 0, 882, 1, '2026-07-05 16:04:51' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607051610511', 2069365345938698241, 40, 0, 357, 0, 357, 1, '2026-07-05 16:10:51' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607051727511', 2069365345938698241, 40, 0, 970, 0, 970, 1, '2026-07-05 17:27:52' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607051751111', 2069365345938698241, 40, 0, 420, 0, 420, 1, '2026-07-05 17:51:12' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607051758501', 2069365345938698241, 40, 0, 406, 859, 1265, 1, '2026-07-05 17:58:51' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607051807301', 2069365345938698241, 40, 0, 1400, 0, 1400, 1, '2026-07-05 18:07:31' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607051810111', 2069365345938698241, 40, 0, 529, 0, 529, 1, '2026-07-05 18:10:11' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607051848211', 2069365345938698241, 40, 0, 3672, 0, 3672, 1, '2026-07-05 18:48:21' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607051853371', 2069365345938698241, 40, 0, 954, 1596, 2550, 1, '2026-07-05 18:53:38' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607051912001', 2069365345938698241, 40, 0, 357, 0, 357, 1, '2026-07-05 19:12:01' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607051924201', 2069365345938698241, 40, 0, 781, 0, 781, 1, '2026-07-05 19:24:21' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607051930061', 2069365345938698241, 40, 0, 1170, 0, 1170, 1, '2026-07-05 19:30:06' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607051943361', 2069365345938698241, 40, 0, 560, 0, 560, 1, '2026-07-05 19:43:36' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607051943511', 2069365345938698241, 40, 0, 630, 0, 630, 1, '2026-07-05 19:43:51' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607051947251', 2069365345938698241, 40, 0, 1120, 0, 1120, 1, '2026-07-05 19:47:26' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607052017561', 2069365345938698241, 40, 0, 357, 0, 357, 1, '2026-07-05 20:17:56' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607052018211', 2069365345938698241, 40, 0, 945, 0, 945, 1, '2026-07-05 20:18:22' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607052023201', 2069365345938698241, 50, 0, 781, 781, 0, 1, '2026-07-05 20:23:21' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607052027551', 2069365345938698241, 40, 0, 518, 0, 518, 1, '2026-07-05 20:27:56' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607052034091', 2069365345938698241, 50, 0, 357, 357, 0, 1, '2026-07-05 20:34:09' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607061003551', 2069365345938698241, 40, 0, 581, 0, 581, 1, '2026-07-06 10:03:56' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607061058461', 2069365345938698241, 40, 0, 564, 0, 564, 1, '2026-07-06 10:58:46' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607061100061', 2069365345938698241, 40, 0, 1274, 0, 1274, 1, '2026-07-06 11:00:06' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607061106461', 2069365345938698241, 40, 0, 1397, 0, 1397, 1, '2026-07-06 11:06:46' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607061114561', 2069365345938698241, 40, 0, 509, 0, 509, 1, '2026-07-06 11:14:56' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607061148561', 2069365345938698241, 40, 0, 357, 0, 357, 1, '2026-07-06 11:48:57' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607061434121', 2069365345938698241, 40, 0, 1316, 6605, 7921, 1, '2026-07-06 14:34:12' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607061553081', 2069365345938698241, 50, 0, 529, 529, 0, 1, '2026-07-06 15:53:09' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607061604001', 2069365345938698241, 50, 0, 480, 490, 10, 1, '2026-07-06 16:04:00' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607061620361', 2069365345938698241, 50, 0, 3672, 3672, 0, 1, '2026-07-06 16:20:36' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607061632241', 2069365345938698241, 50, 0, 100, 100, 0, 1, '2026-07-06 16:32:25' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607061724411', 2069365345938698241, 40, 0, 3329, 0, 3329, 1, '2026-07-06 17:24:41' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607061740311', 2069365345938698241, 40, 0, 1890, 2345, 4235, 1, '2026-07-06 17:40:32' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607061740321', 2069365345938698241, 40, 0, 2590, 4235, 6825, 1, '2026-07-06 17:40:32' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607061819071', 2069365345938698241, 50, 0, 389, 389, 0, 1, '2026-07-06 18:19:07' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607061944461', 2069365345938698241, 40, 0, 1043, 0, 1043, 1, '2026-07-06 19:44:46' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607061953161', 2069365345938698241, 40, 0, 823, 0, 823, 1, '2026-07-06 19:53:16' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607062006451', 2069365345938698241, 40, 0, 1120, 0, 1120, 1, '2026-07-06 20:06:46' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607062011471', 2071977701136384001, 40, 0, 896, 0, 896, 1, '2026-07-06 20:11:47' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607062109341', 2069365345938698241, 50, 0, 919, 921, 2, 1, '2026-07-06 21:09:35' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607062241291', 2069365345938698241, 50, 0, 1120, 1120, 0, 1, '2026-07-06 22:41:30' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071043111', 2069365345938698241, 40, 0, 462, 0, 462, 1, '2026-07-07 10:43:12' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071112271', 2069365345938698241, 40, 0, 560, 0, 560, 1, '2026-07-07 11:12:27' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071115161', 2069365345938698241, 40, 0, 893, 0, 893, 1, '2026-07-07 11:15:16' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071127311', 2069365345938698241, 40, 0, 595, 0, 595, 1, '2026-07-07 11:27:31' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071203511', 2071977701136384001, 40, 0, 399, 0, 399, 1, '2026-07-07 12:03:51' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071204401', 2069365345938698241, 40, 0, 840, 0, 840, 1, '2026-07-07 12:04:41' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071306001', 2071977701136384001, 40, 0, 630, 0, 630, 1, '2026-07-07 13:06:01' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071345051', 2071977701136384001, 40, 0, 1288, 0, 1288, 1, '2026-07-07 13:45:06' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071408001', 2069365345938698241, 40, 0, 840, 0, 840, 1, '2026-07-07 14:08:01' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071420361', 2071977701136384001, 40, 0, 1638, 0, 1638, 1, '2026-07-07 14:20:36' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071423561', 2069365345938698241, 40, 0, 1680, 0, 1680, 1, '2026-07-07 14:23:56' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071435001', 2069365345938698241, 40, 0, 945, 1, 946, 1, '2026-07-07 14:35:01' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071516261', 2069365345938698241, 50, 0, 100, 10000, 9900, 1, '2026-07-07 15:16:27' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071520301', 2069365345938698241, 50, 0, 100, 9900, 9800, 1, '2026-07-07 15:20:30' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071530561', 2071977701136384001, 40, 0, 357, 0, 357, 1, '2026-07-07 15:30:56' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 杭州总部测试 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071544311', 3, 50, 0, 100, 570030, 569930, 1, '2026-07-07 15:44:32' FROM pay_fund WHERE fund_type=10 AND org_id=3 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071545351', 2069365345938698241, 50, 0, 100, 9800, 9700, 1, '2026-07-07 15:45:35' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071558381', 2069365345938698241, 50, 0, 100, 9700, 9600, 1, '2026-07-07 15:58:38' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=9
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071558382', 2069365345938698241, 50, 0, 100, 9600, 9700, 1, '2026-07-07 15:58:39' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071600111', 2069365345938698241, 50, 0, 100, 9700, 9600, 1, '2026-07-07 16:00:12' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=9
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071600121', 2069365345938698241, 50, 0, 100, 9600, 9700, 1, '2026-07-07 16:00:12' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 常州分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071638171', 2071977701136384001, 50, 0, 1288, 1288, 0, 1, '2026-07-07 16:38:17' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071648451', 2069365345938698241, 40, 0, 539, 0, 539, 1, '2026-07-07 16:48:46' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071701551', 2069365345938698241, 50, 0, 777, 777, 0, 1, '2026-07-07 17:01:56' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071704371', 2069365345938698241, 50, 0, 1397, 1397, 0, 1, '2026-07-07 17:04:37' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071711051', 2069365345938698241, 40, 0, 1456, 0, 1456, 1, '2026-07-07 17:11:06' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071712471', 2069365345938698241, 40, 0, 3640, 0, 3640, 1, '2026-07-07 17:12:47' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071806261', 2069365345938698241, 40, 0, 1120, 20, 1140, 1, '2026-07-07 18:06:26' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071807271', 2069365345938698241, 50, 0, 100, 9700, 9600, 1, '2026-07-07 18:07:27' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=9
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071807272', 2069365345938698241, 50, 0, 100, 9600, 9700, 1, '2026-07-07 18:07:28' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071822181', 2069365345938698241, 50, 0, 840, 840, 0, 1, '2026-07-07 18:22:19' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071831261', 2069365345938698241, 50, 0, 100, 9700, 9600, 1, '2026-07-07 18:31:26' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=9
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071831262', 2069365345938698241, 50, 0, 100, 9600, 9700, 1, '2026-07-07 18:31:26' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071832181', 2069365345938698241, 50, 0, 100, 9700, 9600, 1, '2026-07-07 18:32:18' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=9
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071832182', 2069365345938698241, 50, 0, 100, 9600, 9700, 1, '2026-07-07 18:32:18' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071833281', 2069365345938698241, 50, 0, 100, 9700, 9600, 1, '2026-07-07 18:33:28' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=9
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071833282', 2069365345938698241, 50, 0, 100, 9600, 9700, 1, '2026-07-07 18:33:29' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071834261', 2069365345938698241, 40, 0, 812, 0, 812, 1, '2026-07-07 18:34:26' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071837501', 2069365345938698241, 50, 0, 110, 9700, 9590, 1, '2026-07-07 18:37:50' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071840141', 2069365345938698241, 50, 0, 120, 9590, 9470, 1, '2026-07-07 18:40:15' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071841251', 2069365345938698241, 50, 0, 130, 9470, 9340, 1, '2026-07-07 18:41:26' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071843231', 2069365345938698241, 50, 0, 100, 9340, 9240, 1, '2026-07-07 18:43:23' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071844291', 2069365345938698241, 50, 0, 110, 9240, 9130, 1, '2026-07-07 18:44:30' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=9
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071844301', 2069365345938698241, 50, 0, 110, 9130, 9240, 1, '2026-07-07 18:44:30' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071850331', 2069365345938698241, 50, 0, 100, 9240, 9140, 1, '2026-07-07 18:50:34' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=9
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071850341', 2069365345938698241, 50, 0, 100, 9140, 9240, 1, '2026-07-07 18:50:34' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071857021', 2069365345938698241, 50, 0, 100, 9240, 9140, 1, '2026-07-07 18:57:03' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=9
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071857041', 2069365345938698241, 50, 0, 100, 9140, 9240, 1, '2026-07-07 18:57:04' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071859061', 2071977701136384001, 40, 0, 1400, 0, 1400, 1, '2026-07-07 18:59:07' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071903021', 2071977701136384001, 40, 0, 2450, 0, 2450, 1, '2026-07-07 19:03:03' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071908171', 2069365345938698241, 50, 0, 100, 9240, 9140, 1, '2026-07-07 19:08:18' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=9
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071908181', 2069365345938698241, 50, 0, 100, 9140, 9240, 1, '2026-07-07 19:08:19' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071911581', 2069365345938698241, 50, 0, 100, 9240, 9140, 1, '2026-07-07 19:11:58' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=9
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071911591', 2069365345938698241, 50, 0, 100, 9140, 9240, 1, '2026-07-07 19:12:00' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071915481', 2069365345938698241, 50, 0, 200, 9240, 9040, 1, '2026-07-07 19:15:49' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=9
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071915491', 2069365345938698241, 50, 0, 200, 9040, 9240, 1, '2026-07-07 19:15:49' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071922571', 2069365345938698241, 40, 0, 511, 0, 511, 1, '2026-07-07 19:22:57' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607071940111', 2069365345938698241, 40, 0, 2912, 0, 2912, 1, '2026-07-07 19:40:11' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607072003361', 2071977701136384001, 40, 0, 525, 0, 525, 1, '2026-07-07 20:03:37' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607072028511', 2071977701136384001, 40, 0, 980, 0, 980, 1, '2026-07-07 20:28:51' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607072100511', 2071977701136384001, 40, 0, 1260, 0, 1260, 1, '2026-07-07 21:00:51' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607072229351', 2069365345938698241, 50, 0, 100, 9240, 9140, 1, '2026-07-07 22:29:35' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607072231081', 2069365345938698241, 50, 0, 110, 9140, 9030, 1, '2026-07-07 22:31:09' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607072233421', 2069365345938698241, 50, 0, 120, 9030, 8910, 1, '2026-07-07 22:33:42' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607080333351', 2069365345938698241, 50, 0, 1760, 1761, 1, 1, '2026-07-08 03:33:36' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 常州分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607080835561', 2071977701136384001, 50, 0, 525, 525, 0, 1, '2026-07-08 08:35:57' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607080841281', 2069365345938698241, 50, 0, 3640, 3640, 0, 1, '2026-07-08 08:41:28' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607081035461', 2069365345938698241, 40, 0, 858, 0, 858, 1, '2026-07-08 10:35:46' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607081211211', 2069365345938698241, 40, 0, 1470, 5569, 7039, 1, '2026-07-08 12:11:21' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607081211201', 2069365345938698241, 40, 0, 2240, 3329, 5569, 1, '2026-07-08 12:11:21' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607081235001', 2069365345938698241, 50, 0, 800, 805, 5, 1, '2026-07-08 12:35:00' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607081313411', 2069365345938698241, 40, 0, 636, 0, 636, 1, '2026-07-08 13:13:41' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607081408351', 2069365345938698241, 40, 0, 3500, 0, 3500, 1, '2026-07-08 14:08:36' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607081606311', 2069365345938698241, 40, 0, 3857, 3500, 7357, 1, '2026-07-08 16:06:31' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607081615501', 2069365345938698241, 50, 0, 1100, 1140, 40, 1, '2026-07-08 16:15:50' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607081631561', 2069365345938698241, 40, 0, 819, 0, 819, 1, '2026-07-08 16:31:56' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607081736161', 2069365345938698241, 40, 0, 1330, 7039, 8369, 1, '2026-07-08 17:36:16' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607081813411', 2071977701136384001, 40, 0, 672, 0, 672, 1, '2026-07-08 18:13:41' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607081853581', 2069365345938698241, 50, 0, 595, 595, 0, 1, '2026-07-08 18:53:59' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607081917121', 2069365345938698241, 40, 0, 1026, 0, 1026, 1, '2026-07-08 19:17:13' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607081925231', 2069365345938698241, 50, 0, 100, 8910, 8810, 1, '2026-07-08 19:25:24' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607081929031', 2069365345938698241, 50, 0, 100, 8810, 8710, 1, '2026-07-08 19:29:04' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607081932171', 2069365345938698241, 40, 0, 735, 0, 735, 1, '2026-07-08 19:32:17' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607082024011', 2071977701136384001, 40, 0, 1015, 0, 1015, 1, '2026-07-08 20:24:01' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607082029021', 2071977701136384001, 40, 0, 3080, 0, 3080, 1, '2026-07-08 20:29:02' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607082135031', 2069365345938698241, 50, 0, 100, 8710, 8610, 1, '2026-07-08 21:35:03' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607082136331', 2069365345938698241, 50, 0, 100, 8610, 8510, 1, '2026-07-08 21:36:33' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607090720311', 2069365345938698241, 50, 0, 1680, 1680, 0, 1, '2026-07-09 07:20:32' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607091007071', 2071977701136384001, 40, 0, 2121, 3080, 5201, 1, '2026-07-09 10:07:07' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607091007072', 2071977701136384001, 40, 0, 2520, 5201, 7721, 1, '2026-07-09 10:07:07' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607091007111', 2071977701136384001, 40, 0, 2310, 7721, 10031, 1, '2026-07-09 10:07:11' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607091112121', 2069365345938698241, 50, 0, 7920, 7921, 1, 1, '2026-07-09 11:12:13' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607091158211', 2069365345938698241, 40, 0, 480, 0, 480, 1, '2026-07-09 11:58:21' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607091258411', 2071977701136384001, 40, 0, 1050, 0, 1050, 1, '2026-07-09 12:58:41' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607091304301', 2071977701136384001, 40, 0, 364, 0, 364, 1, '2026-07-09 13:04:31' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607091347361', 2069365345938698241, 40, 0, 419, 0, 419, 1, '2026-07-09 13:47:36' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607091419311', 2069365345938698241, 40, 0, 1141, 0, 1141, 1, '2026-07-09 14:19:31' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607091522261', 2069365345938698241, 40, 0, 826, 0, 826, 1, '2026-07-09 15:22:27' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607091550391', 2069365345938698241, 50, 0, 819, 819, 0, 1, '2026-07-09 15:50:39' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607091616001', 2069365345938698241, 40, 0, 1719, 0, 1719, 1, '2026-07-09 16:16:01' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607091621201', 2069365345938698241, 40, 0, 770, 0, 770, 1, '2026-07-09 16:21:21' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607091647511', 2069365345938698241, 40, 0, 1719, 0, 1719, 1, '2026-07-09 16:47:51' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607091719561', 2069365345938698241, 40, 0, 805, 0, 805, 1, '2026-07-09 17:19:57' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607091813211', 2069365345938698241, 40, 0, 1533, 0, 1533, 1, '2026-07-09 18:13:21' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607091822211', 2069365345938698241, 40, 0, 1610, 0, 1610, 1, '2026-07-09 18:22:22' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607091827411', 2069365345938698241, 40, 0, 2100, 0, 2100, 1, '2026-07-09 18:27:42' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607091829301', 2069365345938698241, 40, 0, 770, 5, 775, 1, '2026-07-09 18:29:31' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607091831561', 2069365345938698241, 40, 0, 994, 0, 994, 1, '2026-07-09 18:31:56' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607091901561', 2069365345938698241, 40, 0, 781, 1, 782, 1, '2026-07-09 19:01:56' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607091913181', 2069365345938698241, 50, 0, 994, 994, 0, 1, '2026-07-09 19:13:18' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607091913241', 2069365345938698241, 50, 0, 1600, 1610, 10, 1, '2026-07-09 19:13:25' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607091923321', 2069365345938698241, 50, 0, 480, 480, 0, 1, '2026-07-09 19:23:32' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607091923461', 2069365345938698241, 40, 0, 357, 0, 357, 1, '2026-07-09 19:23:46' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607091936261', 2069365345938698241, 40, 0, 840, 1551, 2391, 1, '2026-07-09 19:36:26' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607092021221', 2071977701136384001, 40, 0, 490, 0, 490, 1, '2026-07-09 20:21:22' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607092025111', 2069365345938698241, 40, 0, 886, 0, 886, 1, '2026-07-09 20:25:12' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607092049161', 2069365345938698241, 40, 0, 795, 0, 795, 1, '2026-07-09 20:49:16' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607092247131', 2069365345938698241, 50, 0, 100, 8510, 8410, 1, '2026-07-09 22:47:14' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607101010371', 2071977701136384001, 40, 0, 2097, 0, 2097, 1, '2026-07-10 10:10:37' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607101135061', 2069365345938698241, 40, 0, 574, 0, 574, 1, '2026-07-10 11:35:07' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607101305001', 2069365345938698241, 40, 0, 525, 0, 525, 1, '2026-07-10 13:05:01' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607101425061', 2069365345938698241, 40, 0, 357, 700, 1057, 1, '2026-07-10 14:25:07' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607101441114', 2069365345938698241, 40, 0, 2100, 3780, 5880, 1, '2026-07-10 14:41:11' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607101441112', 2069365345938698241, 40, 0, 1400, 2030, 3430, 1, '2026-07-10 14:41:11' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607101441111', 2069365345938698241, 40, 0, 1750, 2030, 3780, 1, '2026-07-10 14:41:11' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607101441101', 2069365345938698241, 40, 0, 2030, 0, 2030, 1, '2026-07-10 14:41:11' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W2026071014411110', 2069365345938698241, 40, 0, 1820, 7280, 9100, 1, '2026-07-10 14:41:12' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607101441116', 2069365345938698241, 40, 0, 1680, 3780, 5460, 1, '2026-07-10 14:41:12' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607101441118', 2069365345938698241, 40, 0, 2100, 5180, 7280, 1, '2026-07-10 14:41:12' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607101441122', 2069365345938698241, 40, 0, 1470, 12880, 14350, 1, '2026-07-10 14:41:13' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607101510031', 2069365345938698241, 50, 0, 1533, 1533, 0, 1, '2026-07-10 15:10:03' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607101513491', 2069365345938698241, 50, 0, 357, 357, 0, 1, '2026-07-10 15:13:50' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607101519111', 2069365345938698241, 50, 0, 574, 574, 0, 1, '2026-07-10 15:19:11' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=9
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607101541341', 2069365345938698241, 50, 0, 14350, 0, 14350, 1, '2026-07-10 15:41:34' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607101541331', 2069365345938698241, 50, 0, 14350, 14350, 0, 1, '2026-07-10 15:41:34' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607101543321', 2069365345938698241, 50, 0, 14350, 14350, 0, 1, '2026-07-10 15:43:33' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607101620171', 2069365345938698241, 40, 0, 721, 0, 721, 1, '2026-07-10 16:20:18' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607101643211', 2069365345938698241, 40, 0, 2100, 0, 2100, 1, '2026-07-10 16:43:22' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607101734161', 2069365345938698241, 40, 0, 560, 0, 560, 1, '2026-07-10 17:34:16' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607101810411', 2071977701136384001, 40, 0, 365, 0, 365, 1, '2026-07-10 18:10:41' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 常州分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607101817411', 2071977701136384001, 50, 0, 2097, 2097, 0, 1, '2026-07-10 18:17:42' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607101826501', 2071977701136384001, 40, 0, 1715, 0, 1715, 1, '2026-07-10 18:26:51' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607101826511', 2071977701136384001, 40, 0, 1421, 1715, 3136, 1, '2026-07-10 18:26:52' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607101827301', 2069365345938698241, 40, 0, 459, 0, 459, 1, '2026-07-10 18:27:31' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607101854101', 2069365345938698241, 40, 0, 1050, 0, 1050, 1, '2026-07-10 18:54:11' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607101916161', 2071977701136384001, 40, 0, 1439, 0, 1439, 1, '2026-07-10 19:16:16' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607101928561', 2069365345938698241, 40, 0, 938, 2590, 3528, 1, '2026-07-10 19:28:56' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607101938361', 2071977701136384001, 40, 0, 1782, 0, 1782, 1, '2026-07-10 19:38:36' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607101945211', 2071977701136384001, 40, 0, 632, 0, 632, 1, '2026-07-10 19:45:21' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607102009461', 2069365345938698241, 40, 0, 420, 0, 420, 1, '2026-07-10 20:09:46' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607102012361', 2069365345938698241, 50, 0, 2100, 2100, 0, 1, '2026-07-10 20:12:37' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607102021501', 2069365345938698241, 40, 0, 665, 0, 665, 1, '2026-07-10 20:21:51' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607102024411', 2069365345938698241, 40, 0, 2100, 0, 2100, 1, '2026-07-10 20:24:41' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607102030191', 2069365345938698241, 50, 0, 2100, 2100, 0, 1, '2026-07-10 20:30:20' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607102043011', 2069365345938698241, 40, 0, 1610, 0, 1610, 1, '2026-07-10 20:43:01' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607102331031', 2069365345938698241, 50, 0, 525, 525, 0, 1, '2026-07-10 23:31:04' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111022521', 2071977701136384001, 40, 0, 882, 0, 882, 1, '2026-07-11 10:22:52' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111026263', 2071977701136384001, 40, 0, 1099, 672, 1771, 1, '2026-07-11 10:26:27' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111026261', 2071977701136384001, 40, 0, 672, 0, 672, 1, '2026-07-11 10:26:27' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111039451', 2071977701136384001, 40, 0, 1176, 0, 1176, 1, '2026-07-11 10:39:46' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 杭州总部测试 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111108211', 3, 40, 0, 50000, 569930, 619930, 1, '2026-07-11 11:08:22' FROM pay_fund WHERE fund_type=10 AND org_id=3 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111134461', 2069365345938698241, 50, 0, 1400, 1407, 7, 1, '2026-07-11 11:34:47' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111146161', 2071977701136384001, 40, 0, 1610, 0, 1610, 1, '2026-07-11 11:46:16' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 杭州总部测试 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111147441', 3, 40, 0, 3000, 619930, 622930, 1, '2026-07-11 11:47:44' FROM pay_fund WHERE fund_type=10 AND org_id=3 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111152261', 2069365345938698241, 40, 0, 392, 0, 392, 1, '2026-07-11 11:52:27' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111200311', 2069365345938698241, 40, 0, 700, 560, 1260, 1, '2026-07-11 12:00:31' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111208191', 2069365345938698241, 50, 0, 1260, 1260, 0, 1, '2026-07-11 12:08:20' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111212161', 2071977701136384001, 40, 0, 875, 0, 875, 1, '2026-07-11 12:12:16' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111214461', 2071977701136384001, 40, 0, 361, 0, 361, 1, '2026-07-11 12:14:46' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111215001', 2069365345938698241, 40, 0, 2100, 0, 2100, 1, '2026-07-11 12:15:01' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111218301', 2071977701136384001, 40, 0, 420, 0, 420, 1, '2026-07-11 12:18:31' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111257551', 2069365345938698241, 40, 0, 630, 0, 630, 1, '2026-07-11 12:57:56' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111300001', 2069365345938698241, 40, 0, 973, 0, 973, 1, '2026-07-11 13:00:01' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111311261', 2071977701136384001, 40, 0, 1890, 0, 1890, 1, '2026-07-11 13:11:26' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111329451', 2069365345938698241, 40, 0, 1400, 1610, 3010, 1, '2026-07-11 13:29:46' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111354461', 2069365345938698241, 40, 0, 455, 0, 455, 1, '2026-07-11 13:54:46' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111417061', 2069365345938698241, 40, 0, 1176, 0, 1176, 1, '2026-07-11 14:17:06' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 常州分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111422031', 2071977701136384001, 50, 0, 875, 875, 0, 1, '2026-07-11 14:22:03' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111433111', 2069365345938698241, 40, 0, 840, 0, 840, 1, '2026-07-11 14:33:11' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111510561', 2069365345938698241, 40, 0, 595, 0, 595, 1, '2026-07-11 15:10:56' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111520061', 2069365345938698241, 40, 0, 560, 0, 560, 1, '2026-07-11 15:20:06' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 常州分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111544201', 2071977701136384001, 50, 0, 300, 364, 64, 1, '2026-07-11 15:44:20' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111602311', 2069365345938698241, 50, 0, 413, 413, 0, 1, '2026-07-11 16:02:31' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 常州分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111619111', 2071977701136384001, 40, 0, 1659, 0, 1659, 1, '2026-07-11 16:19:12' FROM pay_fund WHERE fund_type=10 AND org_id=2071977701136384001 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111651061', 2069365345938698241, 40, 0, 732, 0, 732, 1, '2026-07-11 16:51:06' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111721111', 2069365345938698241, 40, 0, 2100, 0, 2100, 1, '2026-07-11 17:21:11' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=8
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111721161', 2069365345938698241, 50, 0, 973, 973, 0, 1, '2026-07-11 17:21:16' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;
-- 温州恒逸分拣中心 bt=11
INSERT INTO pay_fund_flow (pay_fund_id, biz_no, org_id, flow_type, trade_channel, trade_amount, before_balance, after_balance, tenant_id, create_time) SELECT id, 'W202607111723051', 2069365345938698241, 40, 0, 980, 0, 980, 1, '2026-07-11 17:23:06' FROM pay_fund WHERE fund_type=10 AND org_id=2069365345938698241 LIMIT 1;

COMMIT;

-- 公司=1 分拣中心=3 流水=392