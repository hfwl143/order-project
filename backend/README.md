# 接单平台 API 文档

## 启动与测试

在 `backend` 目录启动服务：

```powershell
uv run uvicorn main:app --reload
```

默认地址为 `http://127.0.0.1:8000`，Swagger 文档在 `/docs`，OpenAPI JSON 在 `/openapi.json`。

运行接口回归测试：

```powershell
uv run --group dev python -m pytest -q
```

测试使用内存 SQLite，不会读写 `.env` 配置的业务数据库。

## 通用约定

- 除注册、登录和健康检查外，所有订单接口都需要 `Authorization: Bearer <access_token>`。
- JSON 请求使用 `Content-Type: application/json`。登录接口例外，使用 `application/x-www-form-urlencoded`。
- 成功响应目前使用 HTTP `200`。
- 认证失败返回 `401`；无操作权限返回 `403`；业务状态不允许或参数值不支持通常返回 `400`；请求体类型或必填字段错误返回 `422`。
- 订单标签仅支持：`编程`、`PS设计`、`绘图`、`文案`。
- 订单状态为：`未接单`、`已接单`、`已关闭`。

## 接口列表

| 方法 | 路径 | 认证 | 说明 |
| --- | --- | --- | --- |
| GET | `/api/` | 否 | 服务根信息 |
| GET | `/api/health` | 否 | 健康检查 |
| POST | `/api/register` | 否 | 注册并签发访问令牌 |
| POST | `/api/login` | 否 | 登录并签发访问令牌 |
| GET | `/api/users/me` | 是 | 查看我的联系方式资料 |
| PATCH | `/api/users/me` | 是 | 更新我的微信/手机号 |
| POST | `/api/orders` | 是 | 发布订单 |
| GET | `/api/orders` | 是 | 订单大厅，可按标签筛选 |
| GET | `/api/orders/mine` | 是 | 查看我发布或接取的订单 |
| POST | `/api/orders/{order_id}/take` | 是 | 接单 |
| PUT | `/api/orders/{order_id}` | 是 | 编辑未接单的本人订单 |
| POST | `/api/orders/{order_id}/abandon` | 是 | 接单者申请放弃 |
| POST | `/api/orders/{order_id}/abandon/{decision}` | 是 | 发布者同意或拒绝放弃申请 |
| POST | `/api/orders/{order_id}/close` | 是 | 发布者关闭未接单订单 |

## 认证

### 注册

`POST /api/register`

请求 JSON：

```json
{
	"username": "alice",
	"password": "secret123"
}
```

密码至少 6 个字符；用户名重复或密码过短返回 `400`。成功响应：

```json
{
	"access_token": "<JWT>",
	"token_type": "bearer"
}
```

### 登录

`POST /api/login`

请求表单字段：`username`、`password`。成功响应与注册相同；用户名或密码错误返回 `401`。

PowerShell 示例：

```powershell
curl.exe -X POST http://127.0.0.1:8000/api/login `
	-H "Content-Type: application/x-www-form-urlencoded" `
	-d "username=alice&password=secret123"
```

后续请求带上登录返回的令牌：

```text
Authorization: Bearer <JWT>
```

## 个人联系方式

微信和手机号均为选填，注册时不需要提供；用户随时可通过以下接口维护。联系方式**不会出现在订单大厅**，仅在订单状态为 `已接单` 时，随订单详情的 `contact` 字段向该订单的对方公开（见订单响应字段说明）。

### 查看我的资料

`GET /api/users/me`

```json
{
	"username": "alice",
	"wechat": "alice_design",
	"phone": "13800138000"
}
```

未填写的字段返回 `null`。

### 更新微信/手机号

`PATCH /api/users/me`

```json
{
	"wechat": "alice_design",
	"phone": "13800138000"
}
```

- 两个字段都可省略；传入空字符串表示清空该字段。
- `wechat`：需以字母开头，为 6-20 位字母、数字、下划线或减号。
- `phone`：11 位大陆手机号（`1[3-9]` 开头）。
- 格式不正确返回 `400`，响应示例：`{"detail": "请输入正确的 11 位大陆手机号"}`。

## 订单

### 创建订单

`POST /api/orders`

请求 JSON：

```json
{
	"title": "制作活动海报",
	"description": "需要一张活动宣传海报",
	"tag": "PS设计",
	"deadline": "2026-12-31 18:00"
}
```

`title`、`description`、`tag` 必填；`deadline` 可省略或传 `null`。截止时间当前是普通字符串，没有日期格式校验。

订单响应字段：

| 字段 | 类型 | 说明 |
| --- | --- | --- |
| `id` | integer | 订单 ID |
| `title` | string | 标题 |
| `description` | string | 描述 |
| `tag` | string | 标签 |
| `deadline` | string 或 null | 截止时间 |
| `order_status` | string | `未接单`、`已接单` 或 `已关闭` |
| `abandon_requested` | boolean | 是否有待处理的放弃申请 |
| `publisher_id` | integer | 发布者用户 ID |
| `taker_id` | integer 或 null | 接单者用户 ID |
| `create_time` | string | 创建时间 |
| `is_mine` | boolean | 当前用户是否为发布者或接单者 |
| `my_role` | string 或 null | 当前用户身份：`publisher`、`taker` 或 null |
| `contact` | object 或 null | 参与者可见的对方联系方式 |

`contact` 对象包含 `wechat` 和 `phone`；仅订单已接单且当前用户是发布者或接单者时返回对象，否则为 `null`。联系方式字段本身也可能为 `null`。

### 订单大厅

`GET /api/orders`

可选查询参数 `tag`，例如 `GET /api/orders?tag=编程`。仅返回状态为 `未接单` 的订单。

### 我的订单

`GET /api/orders/mine?role=published`

`role` 可选，默认 `published`；取值为 `published`（我发布的）或 `taken`（我接取的）。其他值返回 `400`。该接口会包含本人已关闭的订单。

### 接单

`POST /api/orders/{order_id}/take`

仅可接取状态为 `未接单` 的其他用户订单。自己接自己的订单返回 `403`；订单不存在或已被接取返回 `400`。接单成功后状态变为 `已接单`。

### 编辑订单

`PUT /api/orders/{order_id}`

请求体与创建订单相同。仅发布者可编辑，且订单必须仍为 `未接单`；否则返回 `403` 或 `400`。

### 放弃申请与处理

- 接单者申请：`POST /api/orders/{order_id}/abandon`
- 发布者处理：`POST /api/orders/{order_id}/abandon/agree` 或 `/api/orders/{order_id}/abandon/reject`

只有当前接单者能申请，只有发布者能处理。`agree` 会将订单恢复为 `未接单` 并清空接单者；`reject` 保持已接单状态。其他 `decision` 值返回 `400`。

超过 3 天未处理的申请会在订单被接口读取并转换响应时自动同意；当前实现不是后台定时任务，若期间没有相关读取请求，不会在那个时刻自动更新。

### 关闭订单

`POST /api/orders/{order_id}/close`

仅发布者可关闭未接单订单。已接单订单需先走放弃流程；成功后状态为 `已关闭`，关闭订单不会再出现在大厅。

## 健康检查

- `GET /api/` 返回 `{"message":"Hello from backend"}`。
- `GET /api/health` 返回 `{"status":"ok"}`。
