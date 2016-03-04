-- --------------------------------------------------------
-- 主机:                           106.185.40.164
-- 服务器版本:                        5.5.46-0ubuntu0.14.04.2 - (Ubuntu)
-- 服务器操作系统:                      debian-linux-gnu
-- HeidiSQL 版本:                  9.3.0.4984
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;

-- 导出 fetch 的数据库结构
CREATE DATABASE IF NOT EXISTS `fetch` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `fetch`;


-- 导出  表 fetch.event 结构
CREATE TABLE IF NOT EXISTS `event` (
  `watcher_updated` tinyint(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- 数据导出被取消选择。


-- 导出  表 fetch.pool 结构
CREATE TABLE IF NOT EXISTS `pool` (
  `time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `page` longtext NOT NULL,
  `wid` char(64) NOT NULL,
  `keys` longtext NOT NULL,
  `hash` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- 数据导出被取消选择。


-- 导出  表 fetch.stage 结构
CREATE TABLE IF NOT EXISTS `stage` (
  `username` varchar(64) NOT NULL,
  `ip` varchar(64) NOT NULL,
  `token` varchar(64) NOT NULL,
  `logintime` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `expired` int(16) NOT NULL DEFAULT '86400000'
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- 数据导出被取消选择。


-- 导出  表 fetch.user 结构
CREATE TABLE IF NOT EXISTS `user` (
  `uid` int(16) NOT NULL AUTO_INCREMENT,
  `username` varchar(64) DEFAULT NULL,
  `mail` varchar(64) NOT NULL,
  `password` varchar(64) NOT NULL,
  `info` varchar(1024) DEFAULT NULL,
  UNIQUE KEY `mail` (`mail`),
  UNIQUE KEY `username` (`username`),
  KEY `uid` (`uid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- 数据导出被取消选择。


-- 导出  表 fetch.watcher 结构
CREATE TABLE IF NOT EXISTS `watcher` (
  `url` char(255) NOT NULL,
  `wid` char(255) NOT NULL,
  `slot` char(255) NOT NULL,
  `enabled` tinyint(4) DEFAULT NULL,
  UNIQUE KEY `uid` (`wid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- 数据导出被取消选择。
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IF(@OLD_FOREIGN_KEY_CHECKS IS NULL, 1, @OLD_FOREIGN_KEY_CHECKS) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
