# FastAPI + SQLAlchemy — 带登录鉴权的 CRUD 操作手册

> 以后要给任何一张表加 CRUD（带登录隔离），按这个手册来。

---

## 一、你必须理解的三层架构

```
HTTP 请求
   ↓
路由层（main.py）    → 接 HTTP、验登录、调函数、返 HTTP 响应
   ↓
数据层（crud.py）    → 只操作数据库，不关心 HTTP/token/登录
   ↓
模型层（models.py + schemas.py）
    models.py  = 数据库表结构（ORM）
    schemas.py = 请求/响应的数据格式（Pydantic）
```

**核心原则：三层各管各的事，不越界。**

---

## 二、每层的职责速查

| 层 | 负责什么 | 绝不碰什么 |
|---|---|---|
| 路由层 main.py | 解析参数、验登录（`Depends(get_current_user)`）、调 crud、返结果 | 直接操作数据库 |
| 数据层 crud.py | 纯数据库增删改查 | 不知道 token/user/HTTP 是什么 |
| 模型层 schemas.py | 定义"用户能提交哪些字段"和"返回什么给前端" | 不知道数据库 |

---

## 三、给新表加 CRUD 的完整步骤

### 第 1 步：models.py — 定义数据库表

```python
class MyTable(Base):
    __tablename__ = "my_table"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(100), nullable=False)

    # ★ 如果要归属用户，加这两行
    owner_id = Column(Integer, ForeignKey("users.id"))
    owner = relationship("User", back_populates="my_tables")
```

### 第 2 步：schemas.py — 定义请求/响应格式

```python
# --- 创建时用户提交的字段（不含 owner_id！）---
class MyTableCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=100)
    # 其他用户填写的字段...

# --- 更新时用户提交的字段（全部可选）---
class MyTableUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=100)
    # 注意：completed、owner_id 这类系统字段不要放这里

# --- 返回给前端的完整数据 ---
class MyTableOut(BaseModel):
    id: int
    title: str
    created_at: datetime

    class Config:
        from_attributes = True  # 必须加，ORM 才能直接转 response
```

**重要：`Create` 和 `Update` 里只能放用户能填的字段，系统字段（owner_id、created_at 等）绝不放这里。**

### 第 3 步：crud.py — 写纯数据库操作

```python
# ===== 列表 =====
def get_my_tables(db: Session, owner_id: int | None = None):
    if owner_id is not None:
        query = db.query(MyTable).filter(MyTable.owner_id == owner_id)
    else:
        query = db.query(MyTable)
    return query.order_by(MyTable.created_at.desc()).all()

# ===== 单条查询（同时做归属校验）=====
def get_my_table(db: Session, table_id: int, owner_id: int | None = None):
    if owner_id is not None:
        query = db.query(MyTable).filter(MyTable.owner_id == owner_id)
    else:
        query = db.query(MyTable)
    return query.filter(MyTable.id == table_id).first()

# ===== 新建（owner_id 作为单独参数！）=====
def create_my_table(db: Session, obj_in, owner_id: int | None = None):
    db_obj = MyTable(**obj_in.model_dump(), owner_id=owner_id)
    db.add(db_obj)
    db.commit()
    db.refresh(db_obj)
    return db_obj

# ===== 更新（只管写字段，不管归属——归属在路由层已经验过了）=====
def update_my_table(db: Session, db_obj, obj_update):
    for field, value in obj_update.model_dump(exclude_unset=True).items():
        setattr(db_obj, field, value)   # ★ 永远是 3 个参数！
    db.commit()
    db.refresh(db_obj)
    return db_obj

# ===== 删除 =====
def delete_my_table(db: Session, db_obj):
    db.delete(db_obj)
    db.commit()
```

**关键：crud 函数不知道 `user` 是谁，`owner_id` 只是一个普通的 int 参数。**

### 第 4 步：main.py — 写路由（HTTP + 认证）

```python
# ===== 列表 =====
@router.get("/my-tables", response_model=list[schemas.MyTableOut])
def list_my_tables(
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),   # ★ 验登录
):
    return crud.get_my_tables(db, owner_id=user.id)   # ★ 传 owner_id

# ===== 单条 =====
@router.get("/my-tables/{id}", response_model=schemas.MyTableOut)
def read_my_table(
    id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    obj = crud.get_my_table(db, id, user.id)          # ★ 传 user.id 做归属
    if not obj:
        raise HTTPException(status_code=404, detail="不存在")
    return obj

# ===== 新建 =====
@router.post("/my-tables", response_model=schemas.MyTableOut)
def create_my_table(
    obj_in: schemas.MyTableCreate,                     # 用户表单（不含 owner_id）
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    return crud.create_my_table(db, obj_in, owner_id=user.id)  # ★ owner_id 单独传

# ===== 更新 =====
@router.put("/my-tables/{id}", response_model=schemas.MyTableOut)
def update_my_table(
    id: int,
    obj_in: schemas.MyTableUpdate,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    db_obj = crud.get_my_table(db, id, user.id)       # ★ 归属校验
    if not db_obj:
        raise HTTPException(status_code=404, detail="不存在或无权修改")
    return crud.update_my_table(db, db_obj, obj_in)   # 只传 3 个参数

# ===== 删除 =====
@router.delete("/my-tables/{id}", status_code=204)
def delete_my_table(
    id: int,
    db: Session = Depends(get_db),
    user: models.User = Depends(get_current_user),
):
    db_obj = crud.get_my_table(db, id, user.id)
    if not db_obj:
        raise HTTPException(status_code=404, detail="不存在或无权删除")
    crud.delete_my_table(db, db_obj)
```

---

## 四、三个必犯错误（已经踩过的坑）

### 错误 1：Pydantic 模型不允许随便加属性

```python
# ❌ 直接报 ValueError: "TaskCreate" object has no field "owner_id"
task.owner_id = user.id

# ✅ 在 crud 层用 model_dump() + 关键字参数合并
db_obj = models.Task(**task.model_dump(), owner_id=user.id)
```

**为什么？** `TaskCreate` 是用户填的表单——它只认识用户能填的字段。`owner_id` 是系统推导的，必须在模型外部组装。

### 错误 2：setattr 不是 4 个参数

```python
# ❌ TypeError: setattr expected 3 arguments, got 4
setattr(db_task, field, value, owner_id)

# ✅ 永远是 3 个：对象、属性名、值
setattr(db_task, field, value)
```

**为什么不需要 owner_id？** `get_my_table(db, id, user.id)` 在路由层已经验证过了，能走到 update 这步的任务**必然是自己的**，不需要再传。

### 错误 3：路由的路径参数必须有斜杠

```python
# ❌ /tasks/1 永远 404，因为正则要求 /tasks1 才能匹配
@router.get("/tasks{task_id}")

# ✅ /tasks/1 才能匹配
@router.get("/tasks/{task_id}")
```

---

## 五、认证流程一句话总结

```
前端登录 → 后端返回 token
    ↓
前端存 token（localStorage）
    ↓
每次请求带上 Authorization: Bearer <token>
    ↓
Depends(get_current_user) 从 token 里解出 user.id
    ↓
user.id 用于：
  • create：塞进 owner_id
  • get/update/delete：传给 crud.get_task 做归属过滤
```

**`get_current_user` 是怎么工作的？**
1. 从请求头里提取 `Authorization: Bearer xxx` 里的 `xxx`（token）
2. 用 JWT 解密，取出 `user_id`
3. 查数据库，拿到 User 对象
4. 如果 token 无效或过期，抛 401

---

## 六、自检清单（每次改完打勾）

### 新建接口
- [ ] `crud.create_my_table` 接收 `owner_id` 参数了吗？
- [ ] 路由层**没有**写 `obj.owner_id = user.id`（而是传参给 crud）了吗？

### 更新/删除接口
- [ ] 路由层加了 `Depends(get_current_user)` 吗？
- [ ] `get_my_table` 调用时传了 `user.id` 吗？
- [ ] `crud.update_my_table` 的 `setattr` 是 3 个参数吗？

### 列表接口
- [ ] 加了 `Depends(get_current_user)` 吗？
- [ ] `crud.get_my_tables` 调用时传了 `owner_id=user.id` 吗？

### 路由
- [ ] 所有 `/{param}` 的斜杠都写了吗？
- [ ] 改完重启 uvicorn 了吗？

---

## 七、测试命令速查

```bash
# 注册（返回 token）
curl.exe -X POST http://127.0.0.1:8000/api/register \
  -H "Content-Type: application/json" \
  -d '{"username":"test1","password":"123456"}'

# 登录（OAuth2 表单格式）
curl.exe -X POST http://127.0.0.1:8000/api/login \
  -H "Content-Type: application/x-www-form-urlencoded" \
  -d "username=test1&password=123456"

# 带 token 建任务（把 <token> 换成上面返回的 access_token）
curl.exe -X POST http://127.0.0.1:8000/api/tasks \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer <token>" \
  -d '{"title":"买菜"}'

# 不带 token 访问 → 应该 401
curl.exe http://127.0.0.1:8000/api/tasks

# 带 token 查列表（只返回自己的任务）
curl.exe http://127.0.0.1:8000/api/tasks \
  -H "Authorization: Bearer <token>"
```

---

## 八、一句话口诀

**路由层管「你是谁」，crud 层管「怎么查/存」，schema 管「能提交什么」。owner_id 永远不从用户表单来，永远从 token 里推。**
