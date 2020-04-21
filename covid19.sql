/*
Navicat MySQL Data Transfer

Source Server         : myTest
Source Server Version : 80019
Source Host           : localhost:3306
Source Database       : covid19

Target Server Type    : MYSQL
Target Server Version : 80019
File Encoding         : 65001

Date: 2020-04-21 23:10:53
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for covid19
-- ----------------------------
DROP TABLE IF EXISTS `covid19`;
CREATE TABLE `covid19` (
  `name` varchar(255) NOT NULL,
  `parent` varchar(255) DEFAULT NULL,
  `new` varchar(255) DEFAULT NULL,
  `now` varchar(255) DEFAULT NULL,
  `total` varchar(255) DEFAULT NULL,
  `cure` varchar(255) DEFAULT NULL,
  `death` varchar(255) DEFAULT NULL,
  `time` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

-- ----------------------------
-- Table structure for dic_lnglat
-- ----------------------------
DROP TABLE IF EXISTS `dic_lnglat`;
CREATE TABLE `dic_lnglat` (
  `name` varchar(255) NOT NULL,
  `lng` varchar(255) CHARACTER SET utf8 COLLATE utf8_general_ci DEFAULT NULL,
  `lat` varchar(255) DEFAULT NULL,
  `type` int(10) unsigned zerofill DEFAULT NULL,
  PRIMARY KEY (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;
SET FOREIGN_KEY_CHECKS=1;
