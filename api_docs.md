# API 接口文档

**基础地址:** `http://172.26.122.226:48081`
**鉴权方式:** Header `Authorization: Bearer {token}`

---

## 一、认证 (管理后台 - 认证)

### 1.1 账号密码登录
- **POST** `/admin-api/system/auth/login`
- Body: `AuthLoginReqVO` (username, password, captchaVerification)
- Response: `CommonResultAuthLoginRespVO` → `{userId, accessToken, refreshToken, expiresTime}`

### 1.2 短信验证码登录
- **POST** `/admin-api/system/auth/sms-login`
- Body: `AuthSmsLoginReqVO` (mobile, code)
- Response: `CommonResultAuthLoginRespVO`

### 1.3 发送手机验证码
- **POST** `/admin-api/system/auth/send-sms-code`
- Body: `AuthSmsSendReqVO` (mobile, scene, captchaVerification)

### 1.4 社交快捷登录
- **POST** `/admin-api/system/auth/social-login`
- Body: `AuthSocialLoginReqVO` (type, code, state)

### 1.5 刷新令牌
- **POST** `/admin-api/system/auth/refresh-token`
- Query: refreshToken

### 1.6 登出
- **POST** `/admin-api/system/auth/logout`

### 1.7 获取登录用户权限信息
- **GET** `/admin-api/system/auth/get-permission-info`
- Response: `AuthPermissionInfoRespVO` (user, roles, permissions, menus)

### 1.8 社交授权跳转
- **GET** `/admin-api/system/auth/social-auth-redirect`
- Query: type, redirectUri

### 1.9 注册用户
- **POST** `/admin-api/system/auth/register`
- Body: `AuthRegisterReqVO`

### 1.10 重置密码
- **POST** `/admin-api/system/auth/reset-password`
- Body: `AuthResetPasswordReqVO`

---

## 二、用户管理 (管理后台 - 用户)

### 2.1 新增用户
- **POST** `/admin-api/system/user/create`
- Body: `UserSaveReqVO`

### 2.2 修改用户
- **PUT** `/admin-api/system/user/update`
- Body: `UserSaveReqVO`

### 2.3 修改用户状态
- **PUT** `/admin-api/system/user/update-status`
- Body: `UserUpdateStatusReqVO` (id, status)

### 2.4 重置密码
- **PUT** `/admin-api/system/user/update-password`
- Body: `UserUpdatePasswordReqVO`

### 2.5 删除用户
- **DELETE** `/admin-api/system/user/delete`
- Query: id

### 2.6 批量删除用户
- **DELETE** `/admin-api/system/user/delete-list`
- Query: ids[]

### 2.7 获取用户分页
- **GET** `/admin-api/system/user/page`
- Query: username, mobile, status, deptId, roleId, pageNo, pageSize

### 2.8 获取用户详情
- **GET** `/admin-api/system/user/get`
- Query: id

### 2.9 导入用户
- **POST** `/admin-api/system/user/import`
- Query: updateSupport, file

### 2.10 导出用户
- **GET** `/admin-api/system/user/export-excel`

### 2.11 绑定转账账号
- **POST** `/admin-api/system/user/bind-transfer-account`
- Body: `BindTransferAccountReqVO`

### 2.12 用户个人中心 - 获取登录用户信息
- **GET** `/admin-api/system/user/profile/get`

### 2.13 用户个人中心 - 修改个人信息
- **PUT** `/admin-api/system/user/profile/update`

### 2.14 用户个人中心 - 修改个人密码
- **PUT** `/admin-api/system/user/profile/update-password`

---

## 三、OAuth2.0 授权 (管理后台)

### 3.1 获取授权信息
- **GET** `/admin-api/system/oauth2/authorize`
- Query: clientId

### 3.2 申请授权
- **POST** `/admin-api/system/oauth2/authorize`
- Query: response_type, client_id, scope, redirect_uri, auto_approve, state

### 3.3 获取访问令牌
- **POST** `/admin-api/system/oauth2/token`
- Query: grant_type, code, redirect_uri, state, username, password, scope, refresh_token

### 3.4 删除访问令牌
- **DELETE** `/admin-api/system/oauth2/token`
- Query: token

### 3.5 校验访问令牌
- **POST** `/admin-api/system/oauth2/check-token`
- Query: token

### 3.6 令牌分页
- **GET** `/admin-api/system/oauth2-token/page`

---

## 四、角色管理 (管理后台)

### 4.1 创建角色
- **POST** `/admin-api/system/role/create`

### 4.2 修改角色
- **PUT** `/admin-api/system/role/update`

### 4.3 删除角色
- **DELETE** `/admin-api/system/role/delete`

### 4.4 角色分页
- **GET** `/admin-api/system/role/page`

### 4.5 获取角色信息
- **GET** `/admin-api/system/role/get`

---

## 五、权限管理 (管理后台)

### 5.1 赋予用户角色
- **POST** `/admin-api/system/permission/assign-user-role`

### 5.2 赋予角色菜单
- **POST** `/admin-api/system/permission/assign-role-menu`

### 5.3 赋予角色数据权限
- **POST** `/admin-api/system/permission/assign-role-data-scope`

### 5.4 获取用户角色编号列表
- **GET** `/admin-api/system/permission/list-user-roles`

### 5.5 获取角色菜单编号
- **GET** `/admin-api/system/permission/list-role-menus`

---

## 六、运营区域管理 (管理后台 - 运营区域)

### 6.1 创建运营区域
- **POST** `/admin-api/system/operate-area/create`

### 6.2 更新运营区域
- **PUT** `/admin-api/system/operate-area/update`

### 6.3 批量创建
- **POST** `/admin-api/system/operate-area/batch-create`

### 6.4 批量更新
- **POST** `/admin-api/system/operate-area/batch-update`

### 6.5 更新围栏开通状态
- **PUT** `/admin-api/system/operate-area/fence-open-status`
- Query: ids[], status

### 6.6 更新业务开通状态
- **PUT** `/admin-api/system/operate-area/biz-open-status`
- Query: ids[], status

### 6.7 分页查询
- **GET** `/admin-api/system/operate-area/page`

### 6.8 获取详情
- **GET** `/admin-api/system/operate-area/get`

### 6.9 获取全部分区
- **GET** `/admin-api/system/operate-area/area-all`

---

## 七、菜单管理 (管理后台)

### 7.1 创建菜单
- **POST** `/admin-api/system/menu/create`

### 7.2 修改菜单
- **PUT** `/admin-api/system/menu/update`

### 7.3 删除菜单
- **DELETE** `/admin-api/system/menu/delete`

### 7.4 获取菜单列表
- **GET** `/admin-api/system/menu/list`

### 7.5 获取菜单精简列表
- **GET** `/admin-api/system/menu/list-all-simple`

---

## 八、字典 & 部门 & 岗位 (管理后台)

### 8.1 字典类型 CRUD
- **POST/GET** `/admin-api/system/dict-type/create | page | list-all-simple | get`

### 8.2 字典数据 CRUD
- **POST/GET** `/admin-api/system/dict-data/create | page | list-all-simple | get`

### 8.3 部门 CRUD
- **POST/GET** `/admin-api/system/dept/create | list | list-all-simple | get`

### 8.4 岗位 CRUD
- **POST/GET** `/admin-api/system/post/create | page | list-all-simple | get`

---

## 九、公司 & Banner & 通知公告 (管理后台)

### 9.1 公司 CRUD
- `/admin-api/system/company/create | update | page | get`

### 9.2 Banner CRUD
- `/admin-api/system/banner/create | update | page | get`

### 9.3 通知公告 CRUD
- `/admin-api/system/notice/create | update | push | page | get`

---

## 十、短信 & 邮件 & 站内信 (管理后台)

### 10.1 短信渠道 CRUD
- `/admin-api/system/sms-channel/create | update | page | get`

### 10.2 短信模板 CRUD
- `/admin-api/system/sms-template/create | update | send-sms | page | get`

### 10.3 短信回调（阿里云/腾讯云/华为云/七牛云）
- **POST** `/admin-api/system/sms/callback/{aliyun|tencent|huawei|qiniu}`

### 10.4 邮件 & 站内信 CRUD
- 邮件: `/admin-api/system/mail-account | mail-template`
- 站内信: `/admin-api/system/notify-template | notify-message`

---

## 十一、RPC 服务（内部调用）

### 11.1 用户相关 (RPC)
| 接口 | 方法 | 说明 |
|------|------|------|
| `/rpc-api/system/user/get` | GET | 通过用户 ID 查询 |
| `/rpc-api/system/user/list` | GET | 通过 ID 列表查用户们 |
| `/rpc-api/system/user/get-by-mobile` | GET | 通过手机号查询 |
| `/rpc-api/system/user/valid` | GET | 校验用户是否有效 |
| `/rpc-api/system/user/list-by-dept-id` | GET | 按部门查用户 |
| `/rpc-api/system/user/list-by-post-id` | GET | 按岗位查用户 |
| `/rpc-api/system/user/list-by-subordinate` | GET | 查询用户下属 |
| `/rpc-api/system/user/update-status` | PUT | 更新用户状态 |
| `/rpc-api/system/user/create-station-wallet` | POST | 创建网点钱包用户 |
| `/rpc-api/system/user/create-station-manager` | POST | 创建网点管理员 |

### 11.2 OAuth2 令牌 (RPC)
| 接口 | 方法 | 说明 |
|------|------|------|
| `/rpc-api/system/oauth2/token/create` | POST | 创建访问令牌 |
| `/rpc-api/system/oauth2/token/check` | GET | 校验访问令牌 |
| `/rpc-api/system/oauth2/token/refresh` | PUT | 刷新令牌 |
| `/rpc-api/system/oauth2/token/remove` | DELETE | 移除令牌 |

### 11.3 其他 RPC 服务
| 模块 | 接口说明 |
|------|----------|
| 短信验证码 | `/rpc-api/system/oauth2/sms/code/send | use | validate` |
| 短信发送 | `/rpc-api/system/sms/send/send-single-member | send-single-admin` |
| 站内信发送 | `/rpc-api/system/notify/send/send-single-member | send-single-admin` |
| 邮件发送 | `/rpc-api/system/mail/send/send-single-member | send-single-admin` |
| 社交用户 | `/rpc-api/system/social-user/bind | unbind | get-by-user-id | get-by-code` |
| 社交应用 | `/rpc-api/system/social-client/*`（微信小程序二维码/订阅消息/订单发货等）|
| 操作日志 | `/rpc-api/system/operate-log/create | page` |
| 登录日志 | `/rpc-api/system/login-log/create` |
| 字典数据 | `/rpc-api/system/dict-data/get | list | valid` |
| 部门/岗位/角色 | `/rpc-api/system/dept/valid | list | get`, `/rpc-api/system/role/valid`, `/rpc-api/system/post/valid | list` |
| 公司 | `/rpc-api/system/company/get | list` |
| Banner | `/rpc-api/system/banner/get-by-position | get-by-positions` |
| 权限 | `/rpc-api/system/permission/has-any-roles | has-any-permissions | get-dept-data-permission | user-role-id-list-by-role-id` |
| 租户 | `/rpc-api/system/tenant/valid | id-list` |
| 系统测试 | `/rpc-api/system/test/save` |

---

## 十二、App 端接口

### 12.1 获取租户信息
- **GET** `/app-api/system/tenant/get-by-website`

### 12.2 字典数据查询
- **GET** `/app-api/system/dict-data/type`

### 12.3 地区树
- **GET** `/app-api/system/area/tree`

---

## 通用返回结构

```json
{
  "code": 0,
  "msg": "success",
  "data": { ... }
}
```

- `code=0` 表示成功
- 所有需要鉴权的接口在 Header 中携带 `Authorization: Bearer {token}`
