#
#  dbtables.sql
#
#  Simplifies the task of creating all the database tables
#  used by the login system.
#
#  Can be run from command prompt by typing:
#
#  mysql -u yourusername -D yourdatabasename < dbtables.sql
#
#  That's with dbtables.sql in the mysql bin directory, but
#  you can just include the path to dbtables.sql and that's
#  fine too.
#
#  Written by: Jpmaster77 a.k.a. The Grandmaster of C++ (GMC)
#  Last Updated: August 13, 2004
#

#
#  Table structure for users table
#

USE nevalashka;

CREATE TABLE users (
 username varchar(30) primary key,
 password varchar(32),
 userid varchar(32),
 userlevel tinyint(1) unsigned not null,
 email varchar(50),
 timestamp int(11) unsigned not null
);

INSERT INTO nevalashka.users VALUES ('neva', 'f6fdffe48c908deb0f4c3bd36c032e72', '21232f297a57a5a743894a0e4a801fc3', 9, 'neva@lashka.com', 123);

CREATE TABLE publications (
 pub_id varchar(32) primary key,
 userid varchar(32) not null,
 filename varchar(100) not null
);

#
#  Table structure for active users table
#
CREATE TABLE active_users (
 username varchar(30) primary key,
 timestamp int(11) unsigned not null
);


#
#  Table structure for active guests table
#
CREATE TABLE active_guests (
 ip varchar(15) primary key,
 timestamp int(11) unsigned not null
);


#
#  Table structure for banned users table
#
CREATE TABLE banned_users (
 username varchar(30) primary key,
 timestamp int(11) unsigned not null
);
