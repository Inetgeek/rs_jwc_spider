-- 创建数据库
DROP DATABASE IF EXISTS xxx;
CREATE DATABASE xxx DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;
show databases;

-- 创建数据表
USE xxx;

-- 创建jwc表
DROP TABLE IF EXISTS `jwc`;
CREATE TABLE `jwc`
(
    `cid`   CHAR(20)        NOT NULL COMMENT '通知信息id',
    `content` VARCHAR(200)   NOT NULL COMMENT '通知内容',
    `cdate` DATE             NOT NULL COMMENT '通知日期',
    `url`  CHAR(200)         NOT NULL COMMENT '通知url',
    PRIMARY KEY (`cid`)
) COMMENT = '教务处通知表', DEFAULT CHARSET = utf8;

-- 创建xspace表
DROP TABLE IF EXISTS `xspace`;
CREATE TABLE `xspace`
(
    `cid`   CHAR(20)        NOT NULL COMMENT '通知信息id',
    `content` VARCHAR(200)   NOT NULL COMMENT '通知内容',
    `cdate` DATE             NOT NULL COMMENT '通知日期',
    `url`  CHAR(200)         NOT NULL COMMENT '通知url',
    PRIMARY KEY (`cid`)
) COMMENT = '竞赛通知表', DEFAULT CHARSET = utf8;