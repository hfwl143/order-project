# 接单集

![Python](https://img.shields.io/badge/Python-3.13%2B-3776AB?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/API-FastAPI-009688?logo=fastapi&logoColor=white)
![Vue](https://img.shields.io/badge/Frontend-Vue_3-42B883?logo=vuedotjs&logoColor=white)

一个面向需求发布与技能协作的全栈应用。发布者可以创建并管理订单，接单者可以按技能分类发现机会；双方通过明确的订单状态和放弃审批流程完成协作。

## 目录

- [项目功能](#项目功能)
- [技术架构](#技术架构)
- [快速开始](#快速开始)
- [运行测试](#运行测试)
- [部署说明](#部署说明)
- [API 文档](#api-文档)

## 项目功能

- **账号认证**：注册、登录与 JWT Bearer Token 认证。
- **订单大厅**：按编程、PS 设计、绘图、文案筛选待接订单。
- **订单协作**：发布订单、编辑未接单订单、接取他人订单和关闭订单。
- **放弃审批**：接单者提交申请，发布者可以同意或拒绝。
- **联系方式保护**：订单接取后，仅订单参与者可查看对方已填写的联系方式。
- **到期处理**：放弃申请超过 3 天后，会在订单后续读取时自动同意。目前采用读取时检查，并非后台定时任务。

前端包含登录/注册、订单大厅和我的订单页面。订单状态包括 `未接单`、`已接单` 和 `已关闭`。

## 技术架构

| 模块 | 技术 |
| --- | --- |
| Web 前端 | Vue 3、Vue Router、Axios、Element Plus、Vite |
| REST API | Python 3.13+、FastAPI、Pydantic |
| 数据访问 | SQLAlchemy |
| 认证 | JWT、密码哈希 |
| 数据库 | SQLAlchemy 支持的数据库；包含 PyMySQL 驱动，本地可用 SQLite |

```text
Vue 3 SPA ── /api ──> FastAPI ── SQLAlchemy ──> SQLite / MySQL
```

### 目录结构

```text
.
├── backend/
│   ├── main.py               # FastAPI 应用和路由挂载
│   ├── router/               # 认证、订单接口
│   ├── auth.py               # 密码、JWT 和身份依赖
│   ├── crud.py               # 数据访问与业务逻辑
│   ├── database.py           # 数据库引擎与会话
│   ├── models.py             # SQLAlchemy 模型
│   ├── schemas.py            # 请求数据模型
│   ├── tests/                # API 回归测试
│   └── README.md             # API 参考文档
├── frontend/
│   ├── src/api/              # Axios 实例与接口调用
│   ├── src/router/           # 路由与登录守卫
│   ├── src/views/            # 登录、订单大厅、我的订单
│   └── vite.config.js        # 开发服务器及 API 代理
├── data.sql
└── README.md
```

## 快速开始

### 环境要求

- Python 3.13 或更高版本
- [uv](https://docs.astral.sh/uv/)
- Node.js 和 npm
- SQLite（本地开发无需单独安装）或 MySQL

### 1. 配置后端

在 `backend/` 目录创建 `.env`。下面的配置适用于本地 SQLite 开发：

```dotenv
SECRET_KEY=replace-with-a-long-random-secret
ALGORITHM=HS256
TOKEN_EXPIRE_MINUTES=60
DATABASE_URL=sqlite:///./dev.db
```

正式环境必须使用足够随机的 `SECRET_KEY` 和受保护的数据库凭据。`.env` 已加入 `.gitignore`，不要将实际密钥提交到 GitHub。

如果使用 MySQL，将 `DATABASE_URL` 设置为 SQLAlchemy URL，例如：

```dotenv
DATABASE_URL=mysql+pymysql://user:password@127.0.0.1:3306/orders?charset=utf8mb4
```

用户名或密码包含 URL 特殊字符时，需要先进行 URL 编码。应用启动时会根据 SQLAlchemy 模型创建缺失的数据表；当前项目尚未配置迁移工具。

### 2. 启动后端

在仓库根目录打开终端：

```bash
cd backend
uv sync --group dev
uv run uvicorn main:app --reload
```

API 默认地址为 `http://127.0.0.1:8000`。启动后可访问：

- Swagger UI：<http://127.0.0.1:8000/docs>
- OpenAPI JSON：<http://127.0.0.1:8000/openapi.json>
- 健康检查：<http://127.0.0.1:8000/api/health>

### 3. 启动前端

在另一个终端中，从仓库根目录执行：

```bash
cd frontend
npm ci
npm run dev
```

在浏览器打开 Vite 输出的地址，默认是 <http://127.0.0.1:5173>。开发服务器会将 `/api` 请求代理到 `http://127.0.0.1:8000`。

如后端地址不同，在 `frontend/.env.local` 中设置代理目标：

```dotenv
VITE_BACKEND_URL=http://127.0.0.1:8001
```

前端路由：

| 路径 | 页面 | 访问要求 |
| --- | --- | --- |
| `/login` | 登录与注册 | 无 |
| `/` | 订单大厅 | 登录 |
| `/mine` | 我发布的 / 我接取的 | 登录 |

## 运行测试

运行后端 API 回归测试（在 `backend/` 目录执行）：

```bash
uv run --group dev python -m pytest -q
```

测试使用内存 SQLite 并覆盖应用的数据库依赖，不会写入 `.env` 配置的业务数据库。由于应用设置会在导入时读取环境变量，运行测试前仍需准备 `backend/.env`。

构建前端（在 `frontend/` 目录执行）：

```bash
npm run build
```

## 部署说明

Vite 的 `/api` 代理仅用于本地开发。生产部署时，可选择：

1. 由 Nginx、Caddy 或其他 Web 服务器将 `/api` 反向代理到 FastAPI。
2. 构建前设置 `VITE_API_BASE_URL` 为完整 API 前缀，例如 `https://api.example.com/api`。

同时应为前端域名配置 FastAPI CORS 允许来源、使用 HTTPS，并通过环境变量或密钥管理服务提供生产密钥。不要将开发用 `.env`、数据库文件或真实用户数据发布到公开仓库。

## API 文档

接口清单、请求与响应字段、认证要求、业务错误和状态流转见[后端 API 文档](backend/README.md)。
