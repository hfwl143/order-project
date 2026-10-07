-- 接单平台 MySQL 8.0 初始化脚本
-- 仅在数据卷为空（首次启动）时由 docker-entrypoint-initdb.d 自动执行一次
-- 表结构与 backend/models.py 保持一致；后端启动时另有 create_all 兜底补建

CREATE TABLE IF NOT EXISTS users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    hashed_password VARCHAR(200) NOT NULL,
    wechat VARCHAR(100),
    phone VARCHAR(20)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4;

CREATE TABLE IF NOT EXISTS orders (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '订单主键ID',
    title VARCHAR(100) NOT NULL COMMENT '订单标题',
    description TEXT NOT NULL COMMENT '接单需求详细描述',
    tag VARCHAR(20) NOT NULL COMMENT '订单分类标签，如：编程/PS设计/绘图/文案',
    deadline VARCHAR(20) COMMENT '任务截止时间字符串，如 2026-09-30 18:00',
    order_status VARCHAR(20) NOT NULL DEFAULT '未接单' COMMENT '订单状态：未接单/已接单/已关闭',
    abandon_requested TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否申请废弃订单，0否1是',
    abandon_request_time DATETIME COMMENT '提交废弃申请的时间',
    publisher_id INT NOT NULL COMMENT '发布人用户id',
    taker_id INT NULL COMMENT '接单者用户id，未接单为null',
    create_time DATETIME NOT NULL COMMENT '订单创建时间',
    update_time DATETIME NOT NULL COMMENT '订单最后更新时间',
    FOREIGN KEY (publisher_id) REFERENCES users (id),
    FOREIGN KEY (taker_id) REFERENCES users (id)
) ENGINE = InnoDB DEFAULT CHARSET = utf8mb4 COMMENT '接单平台订单表';
