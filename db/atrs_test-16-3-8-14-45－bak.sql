# ************************************************************
# Sequel Pro SQL dump
# Version 4529
#
# http://www.sequelpro.com/
# https://github.com/sequelpro/sequelpro
#
# Host: 127.0.0.1 (MySQL 5.6.21)
# Database: atrs_test
# Generation Time: 2016-03-08 06:45:44 +0000
# ************************************************************


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


# Dump of table T_ACCOUNT
# ------------------------------------------------------------

DROP TABLE IF EXISTS `T_ACCOUNT`;

CREATE TABLE `T_ACCOUNT` (
  `id` int(4) NOT NULL AUTO_INCREMENT,
  `username` char(40) NOT NULL,
  `password` char(40) NOT NULL DEFAULT '',
  `name` char(40) DEFAULT '',
  `is_super` tinyint(1) DEFAULT '0',
  `create_date` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `T_ACCOUNT` WRITE;
/*!40000 ALTER TABLE `T_ACCOUNT` DISABLE KEYS */;

INSERT INTO `T_ACCOUNT` (`id`, `username`, `password`, `name`, `is_super`, `create_date`)
VALUES
	(1,'wm','changed','update_value_by_dict',1,'2015-10-29 00:00:00'),
	(2,'wm','changed2','update_value',0,'2015-10-29 00:00:00'),
	(3,'1','z','',0,NULL),
	(4,'2','bx','',0,NULL),
	(5,'3','c','',0,NULL),
	(6,'4','d','',0,NULL),
	(7,'5','xxs','',0,NULL),
	(8,'6','x','',0,NULL),
	(9,'7','g','',0,NULL),
	(10,'8','n','',0,NULL),
	(11,'9','y','',0,NULL),
	(12,'10','o','',0,NULL),
	(13,'wm','changed','update_value_by_dict',0,'2015-10-29 00:00:00'),
	(14,'wm','changed','update_value_by_dict',2,'2015-10-29 00:00:00');

/*!40000 ALTER TABLE `T_ACCOUNT` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table T_APP
# ------------------------------------------------------------

DROP TABLE IF EXISTS `T_APP`;

CREATE TABLE `T_APP` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` char(40) NOT NULL,
  `status` char(40) NOT NULL DEFAULT 'Down',
  `type` char(40) NOT NULL DEFAULT 'Java',
  `description` text,
  `script` text,
  `access_url` char(100) DEFAULT '',
  `last_release_time` datetime DEFAULT NULL,
  `release_flow` int(11) DEFAULT '0',
  `last_release_status` char(40) DEFAULT 'Failed',
  `last_release_log` char(100) DEFAULT NULL,
  `last_release_info` char(100) DEFAULT NULL,
  `repository_type` char(40) DEFAULT NULL,
  `repository_path` char(100) DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `T_APP` WRITE;
/*!40000 ALTER TABLE `T_APP` DISABLE KEYS */;

INSERT INTO `T_APP` (`id`, `name`, `status`, `type`, `description`, `script`, `access_url`, `last_release_time`, `release_flow`, `last_release_status`, `last_release_log`, `last_release_info`, `repository_type`, `repository_path`)
VALUES
	(1,'amss','Down','JavaWeb','中国高校社科数据中心授权管理与服务系统',NULL,'http://localhost:8080/amss','2016-03-03 10:35:04',0,'Failed','/Users/wangming/workspace/atrs/workbench/release/log/20160303103503-amss.log','access url failed','SVN','https://192.168.88.210/repos/csdc/amss/'),
	(14,'sshdemo_file','Down','JavaWeb','SSH框架，没有maven，Repository Type是File',NULL,'http://localhost:8080/sshdemo_file','2016-03-03 14:52:20',0,'Success','/Users/wangming/workspace/atrs/workbench/release/log/20160303145220-sshdemo_file.log','release the app successfully','File','/Users/wangming/Documents/project/sshdemo');

/*!40000 ALTER TABLE `T_APP` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table T_CASE
# ------------------------------------------------------------

DROP TABLE IF EXISTS `T_CASE`;

CREATE TABLE `T_CASE` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` char(40) NOT NULL DEFAULT '',
  `description` text,
  `param` text,
  `driver` char(40) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `T_CASE` WRITE;
/*!40000 ALTER TABLE `T_CASE` DISABLE KEYS */;

INSERT INTO `T_CASE` (`id`, `name`, `description`, `param`, `driver`)
VALUES
	(15,'case_demo_1','this is a case demo of driver_demo','{}','driver_demo'),
	(24,'case_true','a true case','{\"out\":\"2\",\"in\":\"1\"}','driver_true'),
	(25,'case_true2','this is a successful case','{}','driver_demo');

/*!40000 ALTER TABLE `T_CASE` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table T_CASE_RESULT
# ------------------------------------------------------------

DROP TABLE IF EXISTS `T_CASE_RESULT`;

CREATE TABLE `T_CASE_RESULT` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `case_name` char(40) NOT NULL DEFAULT '',
  `create_time` datetime DEFAULT NULL,
  `status` char(40) DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `stop_time` datetime DEFAULT NULL,
  `log` text,
  `user` char(40) DEFAULT NULL,
  `description` text,
  `result_info` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `T_CASE_RESULT` WRITE;
/*!40000 ALTER TABLE `T_CASE_RESULT` DISABLE KEYS */;

INSERT INTO `T_CASE_RESULT` (`id`, `case_name`, `create_time`, `status`, `start_time`, `stop_time`, `log`, `user`, `description`, `result_info`)
VALUES
	(5,'case_demo_1','2016-01-20 16:14:55','running','2016-01-20 16:35:36',NULL,NULL,NULL,NULL,NULL),
	(6,'case_demo_1','2016-01-20 16:15:19','failed','2016-01-20 16:47:45','2016-01-20 16:47:45','',NULL,NULL,NULL),
	(7,'case_demo_1','2016-01-20 16:17:39','failed','2016-01-20 17:09:32','2016-01-20 17:09:32','/Users/wangming/workspace/atrs/control/../workbench/log/tc_case_demo_1_id_7.log',NULL,NULL,NULL),
	(9,'case_demo_1','2016-01-20 17:13:21','failed','2016-01-20 17:13:21','2016-01-20 17:13:21','/Users/wangming/workspace/atrs/control/../workbench/log/tc_case_demo_1_id_9.log',NULL,NULL,NULL),
	(10,'case_demo_1','2016-01-20 17:14:01','failed','2016-01-20 17:14:01','2016-01-20 17:14:01','/Users/wangming/workspace/atrs/control/../workbench/log/tc_case_demo_1_id_10.log',NULL,NULL,NULL),
	(11,'case_demo_1','2016-01-20 17:18:05','failed','2016-01-20 17:18:05','2016-01-20 17:18:05','/Users/wangming/workspace/atrs/control/../workbench/log/tc_case_demo_1_id_11.log',NULL,NULL,NULL),
	(12,'case_demo_1','2016-01-20 17:18:23','failed','2016-01-20 17:18:24','2016-01-20 17:18:24','/Users/wangming/workspace/atrs/control/../workbench/log/tc_case_demo_1_id_12.log',NULL,NULL,NULL),
	(13,'case_demo_1','2016-01-20 17:19:56','failed','2016-01-20 17:19:56','2016-01-20 17:19:56','/Users/wangming/workspace/atrs/control/../workbench/log/tc_case_demo_1_id_13.log',NULL,NULL,NULL),
	(14,'case_demo_1','2016-01-20 17:20:34','failed','2016-01-20 17:20:34','2016-01-20 17:20:34','/Users/wangming/workspace/atrs/control/../workbench/log/tc_case_demo_1_id_14.log',NULL,NULL,NULL),
	(15,'case_demo_1','2016-01-20 17:20:48','failed','2016-01-20 17:20:48','2016-01-20 17:20:48','/Users/wangming/workspace/atrs/control/../workbench/log/tc_case_demo_1_id_15.log',NULL,NULL,NULL),
	(16,'case_demo_1','2016-01-20 17:20:57','failed','2016-01-20 17:20:57','2016-01-20 17:20:57','/Users/wangming/workspace/atrs/control/../workbench/log/tc_case_demo_1_id_16.log',NULL,NULL,NULL),
	(17,'case_demo_1','2016-01-20 17:21:19','failed','2016-01-20 17:21:19','2016-01-20 17:21:19','/Users/wangming/workspace/atrs/control/../workbench/log/tc_case_demo_1_id_17.log',NULL,NULL,NULL),
	(18,'case_demo_1','2016-01-20 17:21:43','failed','2016-01-20 17:21:43','2016-01-20 17:21:43','/Users/wangming/workspace/atrs/control/../workbench/log/tc_case_demo_1_id_18.log',NULL,NULL,NULL),
	(19,'case_demo_1','2016-01-20 17:21:50','failed','2016-01-20 17:21:50','2016-01-20 17:21:50','/Users/wangming/workspace/atrs/control/../workbench/log/tc_case_demo_1_id_19.log',NULL,NULL,NULL),
	(20,'case_demo_1','2016-01-20 17:22:34','failed','2016-01-20 17:22:34','2016-01-20 17:22:34','/Users/wangming/workspace/atrs/control/../workbench/log/tc_case_demo_1_id_20.log',NULL,NULL,NULL),
	(21,'case_demo_1','2016-01-20 17:23:45','failed','2016-01-20 17:23:45','2016-01-20 17:23:45','/Users/wangming/workspace/atrs/control/../workbench/log/tc_case_demo_1_id_21.log',NULL,NULL,NULL),
	(22,'case_demo_1','2016-03-03 19:29:38','running',NULL,NULL,NULL,NULL,NULL,NULL),
	(23,'case_demo_1','2016-03-03 21:30:03','running',NULL,NULL,NULL,NULL,NULL,NULL),
	(24,'case_demo_1','2016-03-03 21:33:33','running',NULL,NULL,NULL,NULL,NULL,NULL),
	(25,'case_demo_1','2016-03-03 21:46:33','failed','2016-03-03 21:46:34','2016-03-03 21:46:34','/Users/wangming/workspace/atrs/workbench/case/log/tc_case_demo_1_id_25.log',NULL,NULL,NULL),
	(26,'dsfdsf','2016-03-06 14:32:48','running',NULL,NULL,NULL,NULL,NULL,NULL),
	(27,'zzzz','2016-03-06 21:01:14','failed','2016-03-06 21:01:14','2016-03-06 21:01:14','/Users/wangming/workspace/atrs/workbench/case/log/tc_zzzz_id_27.log',NULL,NULL,NULL),
	(28,'case_true','2016-03-06 21:02:35','failed','2016-03-06 21:02:35','2016-03-06 21:02:35','/Users/wangming/workspace/atrs/workbench/case/log/tc_case_true_id_28.log',NULL,NULL,NULL),
	(29,'case_true','2016-03-06 21:24:20','success','2016-03-06 21:24:20','2016-03-06 21:24:20','/Users/wangming/workspace/atrs/workbench/case/log/tc_case_true_id_29.log',NULL,NULL,NULL),
	(30,'case_true','2016-03-07 15:50:48','success','2016-03-07 15:50:48','2016-03-07 15:50:48','/Users/wangming/workspace/atrs/workbench/case/log/tc_case_true_id_30.log',NULL,NULL,NULL),
	(31,'case_true2','2016-03-07 15:50:59','success','2016-03-07 15:50:59','2016-03-07 15:50:59','/Users/wangming/workspace/atrs/workbench/case/log/tc_case_true2_id_31.log',NULL,NULL,NULL);

/*!40000 ALTER TABLE `T_CASE_RESULT` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table T_DRIVER
# ------------------------------------------------------------

DROP TABLE IF EXISTS `T_DRIVER`;

CREATE TABLE `T_DRIVER` (
  `id` int(4) unsigned NOT NULL AUTO_INCREMENT,
  `name` char(40) NOT NULL DEFAULT '',
  `description` text,
  `setuppy` text NOT NULL,
  `teardownpy` text NOT NULL,
  `execpy` text NOT NULL,
  `param` text,
  `user` char(40) NOT NULL DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `T_DRIVER` WRITE;
/*!40000 ALTER TABLE `T_DRIVER` DISABLE KEYS */;

INSERT INTO `T_DRIVER` (`id`, `name`, `description`, `setuppy`, `teardownpy`, `execpy`, `param`, `user`)
VALUES
	(80,'driver_demo','this is a driver demo','def setup(tc):\r\n    pass','def teardown(tc):\r\n    pass','def tc_hello(tc):\r\n    print \'tc_hello\'\r\n    print tc.name\r\n    assert False, \'hello\'\r\ndef tc_bye(tc):\r\n    print \'tc_bye\'\r\n    print tc.age\r\n    assert True, \'bye\'','{}',''),
	(86,'driver_true','successful driver','def setUp(tc):\r\n    pass','def tearDown(tc):\r\n    pass','def runTest(tc):\r\n    assert True','{\"in\":\"1\",\"out\":\"2\"}','');

/*!40000 ALTER TABLE `T_DRIVER` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table T_PLAN
# ------------------------------------------------------------

DROP TABLE IF EXISTS `T_PLAN`;

CREATE TABLE `T_PLAN` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` char(40) NOT NULL DEFAULT '',
  `case_list` text CHARACTER SET utf8 COLLATE utf8_bin NOT NULL,
  `people` text,
  `crontab` char(100) DEFAULT '',
  `last_status` char(40) DEFAULT '',
  `description` text,
  `user` char(40) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `T_PLAN` WRITE;
/*!40000 ALTER TABLE `T_PLAN` DISABLE KEYS */;

INSERT INTO `T_PLAN` (`id`, `name`, `case_list`, `people`, `crontab`, `last_status`, `description`, `user`)
VALUES
	(5,'plan_demo',X'74635F636173655F64656D6F5F31','374806534@qq.com','','','',NULL),
	(8,'plantrue',X'636173655F747275652C636173655F7472756532','378406534@qq.com;378406534@qq.com','','','this a successful plan',NULL),
	(9,'ppppp',X'636173655F747275652C636173655F7472756532','378406534@qq.com,378406534@qq.com','','','',NULL),
	(10,'p_l_a_n',X'636173655F747275652C636173655F7472756532','378406534@qq.com,378406534@qq.com	','','','',NULL),
	(11,'plan_true',X'636173655F747275652C636173655F7472756532','378406534@qq.com','','','',NULL),
	(12,'plan_true_sdfsdf',X'636173655F747275652C636173655F7472756532','378406534@qq.com,378406534@qq.com','','','',NULL);

/*!40000 ALTER TABLE `T_PLAN` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table T_PLAN_RESULT
# ------------------------------------------------------------

DROP TABLE IF EXISTS `T_PLAN_RESULT`;

CREATE TABLE `T_PLAN_RESULT` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `plan_name` char(40) DEFAULT NULL,
  `status` char(40) DEFAULT NULL,
  `create_time` datetime DEFAULT NULL,
  `start_time` datetime DEFAULT NULL,
  `stop_time` datetime DEFAULT NULL,
  `type` char(40) DEFAULT '0',
  `log` text,
  `result_info` text,
  `user` char(40) DEFAULT NULL,
  `description` text,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

LOCK TABLES `T_PLAN_RESULT` WRITE;
/*!40000 ALTER TABLE `T_PLAN_RESULT` DISABLE KEYS */;

INSERT INTO `T_PLAN_RESULT` (`id`, `plan_name`, `status`, `create_time`, `start_time`, `stop_time`, `type`, `log`, `result_info`, `user`, `description`)
VALUES
	(1,'plan_demo','failed',NULL,'2016-01-20 22:20:42','2016-01-20 22:20:42','0','/Users/wangming/workspace/atrs/control/../workbench/log/tp_plan_demo_id_1.log',NULL,NULL,NULL),
	(2,'plan_demo','failed',NULL,'2016-01-20 22:20:44','2016-01-20 22:20:44','0','/Users/wangming/workspace/atrs/control/../workbench/log/tp_plan_demo_id_2.log',NULL,NULL,NULL),
	(3,'plan_demo','failed',NULL,'2016-01-20 22:14:59','2016-01-20 22:14:59','0','/Users/wangming/workspace/atrs/control/../workbench/log/tp_plan_demo_id_3.log',NULL,NULL,NULL),
	(4,'plan_demo','failed',NULL,'2016-01-20 22:15:00','2016-01-20 22:15:00','0','/Users/wangming/workspace/atrs/control/../workbench/log/tp_plan_demo_id_4.log',NULL,NULL,NULL),
	(5,'plan_demo','failed',NULL,'2016-01-20 22:15:01','2016-01-20 22:15:01','0','/Users/wangming/workspace/atrs/control/../workbench/log/tp_plan_demo_id_5.log',NULL,NULL,NULL),
	(6,'plan_demo','failed',NULL,'2016-01-20 22:15:02','2016-01-20 22:15:02','0','/Users/wangming/workspace/atrs/control/../workbench/log/tp_plan_demo_id_6.log',NULL,NULL,NULL),
	(7,'plan_demo','failed',NULL,'2016-01-21 09:29:13','2016-01-21 09:29:13','0','/Users/wangming/workspace/atrs/control/../workbench/log/tp_plan_demo_id_7.log',NULL,NULL,NULL),
	(8,'plan_demo','running',NULL,'2016-03-03 19:32:14',NULL,'0',NULL,NULL,NULL,NULL),
	(9,'plan_demo','failed',NULL,'2016-03-04 15:20:42','2016-03-04 15:20:42','0','/Users/wangming/workspace/atrs/workbench/case/log/tp_plan_demo_id_9.log',NULL,NULL,NULL),
	(10,'plan_true','running',NULL,'2016-03-06 21:26:57',NULL,'0',NULL,NULL,NULL,NULL),
	(11,'plan_true','running',NULL,'2016-03-06 21:28:00',NULL,'0',NULL,NULL,NULL,NULL),
	(12,'plantrue','failed',NULL,'2016-03-07 15:49:47','2016-03-07 15:49:47','0','/Users/wangming/workspace/atrs/workbench/case/log/tp_plantrue_id_12.log',NULL,NULL,NULL),
	(13,'ppppp','failed',NULL,'2016-03-07 16:08:28','2016-03-07 16:08:28','0','/Users/wangming/workspace/atrs/workbench/case/log/tp_ppppp_id_13.log',NULL,NULL,NULL),
	(14,'p_l_a_n','success',NULL,'2016-03-07 16:11:19','2016-03-07 16:11:19','0','/Users/wangming/workspace/atrs/workbench/case/log/tp_p_l_a_n_id_14.log',NULL,NULL,NULL),
	(15,'p_l_a_n','success',NULL,'2016-03-07 16:24:53','2016-03-07 16:24:53','0','/Users/wangming/workspace/atrs/workbench/case/log/tp_p_l_a_n_id_15.log',NULL,NULL,NULL),
	(16,'plan_demo','failed',NULL,'2016-03-07 18:29:41','2016-03-07 18:29:41','0','/Users/wangming/workspace/atrs/workbench/case/log/tp_plan_demo_id_16.log',NULL,NULL,NULL);

/*!40000 ALTER TABLE `T_PLAN_RESULT` ENABLE KEYS */;
UNLOCK TABLES;


# Dump of table T_REPORT
# ------------------------------------------------------------

DROP TABLE IF EXISTS `T_REPORT`;

CREATE TABLE `T_REPORT` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `plan` char(40) DEFAULT NULL,
  `status` char(40) DEFAULT NULL,
  `date` datetime DEFAULT NULL,
  `type` int(4) NOT NULL DEFAULT '0',
  `msg` text,
  `user` char(40) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;



# Dump of table T_SYSTEM_OPTION
# ------------------------------------------------------------

DROP TABLE IF EXISTS `T_SYSTEM_OPTION`;

CREATE TABLE `T_SYSTEM_OPTION` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` char(40) NOT NULL DEFAULT '',
  `code` char(40) NOT NULL DEFAULT '',
  `description` char(100) DEFAULT '',
  `standard` char(40) DEFAULT '',
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;




/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;
/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
