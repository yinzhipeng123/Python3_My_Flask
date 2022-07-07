
drop table if exists users;
create table users (
	id integer primary key autoincrement,
	user string not null,
	password string not null
);

drop table if exists entries;
create table entries (
	id integer primary key autoincrement,
	title string not null,
	text string not null,
	author integer not null,
	foreign key(author)  references users(id)
);

PRAGMA foreign_keys = ON;
insert into users values (NULL,'admin','123456');
insert into users values (NULL,'yinzhipeng','123456');

insert into entries values (NULL,'test','test',1);
insert into entries values (NULL,'testyin','testyin',2);
