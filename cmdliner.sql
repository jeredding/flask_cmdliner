drop table if exists cmds;
create table cmds (
  id integer primary key autoincrement,
  title text not null,
  command text not null
);