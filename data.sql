CREATE TABLE users (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) NOT NULL UNIQUE,
    hashed_password VARCHAR(200) NOT NULL
) CHARSET = utf8mb4;

ALTER TABLE tasks ADD COLUMN owner_id INT;

ALTER TABLE tasks ADD FOREIGN KEY (owner_id) REFERENCES users (id);

DROP TABLE tasks;

DROP TABLE IF EXISTS tasks;

ALTER TABLE users ADD COLUMN wechat VARCHAR(100);

ALTER TABLE users ADD COLUMN phone VARCHAR(20);

CREATE TABLE orders (
    id INT AUTO_INCREMENT PRIMARY KEY COMMENT '订单主键ID',
    title VARCHAR(100) NOT NULL COMMENT '订单标题',
    description TEXT NOT NULL COMMENT '接单需求详细描述',
    tag VARCHAR(20) NOT NULL COMMENT '订单分类标签，如：前端、Python、算法',
    deadline DATETIME COMMENT '任务截止时间',
    order_status VARCHAR(20) NOT NULL DEFAULT '未接单' COMMENT '订单状态：未接单/进行中/已完成/已废弃',
    abandon_requested TINYINT(1) NOT NULL DEFAULT 0 COMMENT '是否申请废弃订单，0否1是',
    abandon_request_time DATETIME COMMENT '提交废弃申请的时间',
    publisher_id INT NOT NULL COMMENT '发布人用户id',
    taker_id INT NULL COMMENT '接单者用户id，未接单为null',
    create_time DATETIME NOT NULL COMMENT '订单创建时间',
    update_time DATETIME NOT NULL COMMENT '订单最后更新时间',
    FOREIGN KEY (publisher_id) REFERENCES users (id),
    FOREIGN KEY (taker_id) REFERENCES users (id)
) CHARSET = utf8mb4 COMMENT '接单平台订单表';