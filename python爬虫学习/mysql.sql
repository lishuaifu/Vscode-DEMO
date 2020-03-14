#建表
CREATE TABLE `history`(
	`ds` datetime  NOT NULL comment'日期',
	`confirm` int(11) DEFAULT  NULL COMMENT '累计确诊', 
	`confirm_add` int(11) DEFAULT  NULL COMMENT '当日新增确诊', 
	
	`suspect` int(11) DEFAULT  NULL COMMENT '剩余疑似', 
	`suspect_add` int(11) DEFAULT  NULL COMMENT '当日新增疑似', 
	`heal` int(11) DEFAULT  NULL COMMENT '累计治愈', 
	`heal_add` int(11) DEFAULT  NULL COMMENT '当日新增治愈', 
	`dead` int(11) DEFAULT  NULL COMMENT '累计死亡', 
	`dead_add` int(11) DEFAULT  NULL COMMENT '当日新增死亡', 
	 PRIMARY KEY (`ds`) USING BTREE
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; 多打了一个not



CREATE TABLE `details`(
	 id int(11) not null AUTO_INCREMENT,
	 update_time datetime default null comment '数据最后更新时间',
	 province varchar(50) default null comment '省',
   city varchar(50) default null comment '市',
   confirm int(11) DEFAULT  NULL COMMENT '累计确诊', 
	 confirm_add int(11) DEFAULT  NULL COMMENT '当日新增确诊', 
   `heal` int(11) DEFAULT  NULL COMMENT '累计治愈', 
	 `dead` int(11) DEFAULT  NULL COMMENT '累计死亡', 
		primary key(`id`)
)ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;




create table hostsearch(
	id int(11) not null auto_increment,  主键自增
	dt datetime default null on update CURRENT_TIMESTAMP, 时间戳
	content varchar(255) default null, 爬取到的目标值内容
	PRIMARY key (id)
)ENGINE=INNODB DEFAULT charset=utf8mb4;
