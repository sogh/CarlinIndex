# --- Created by Ebean DDL
# To stop Ebean DDL generation, remove this comment and start using Evolutions

# --- !Ups

create table user (
  name                      varchar(255) not null,
  carlin_index              double,
  top_tweet                 varchar(255),
  constraint pk_user primary key (name))
;




# --- !Downs

SET FOREIGN_KEY_CHECKS=0;

drop table user;

SET FOREIGN_KEY_CHECKS=1;

