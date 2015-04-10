drop table if exists majors_lookup;
drop table if exists course_lookup;
drop table if exists student_account_details;
drop table if exists student_academic_details;
drop table if exists student_course_details;
drop table if exists course_tags;
drop table if exists student_interests;

create table course_tags(
  course_code interger not null,
  tag_name VARCHAR not null,
  FOREIGN KEY (course_code) REFERENCES course_lookup(id)
);


create table student_interests(
  s_id integer not null,
  tag_name VARCHAR not null
);


create table student_course_details(
  id integer not null,
  course_name varchar not null,
  course_code varchar not null,
  semester varchar not null

);

create table student_account_details(
  id integer primary key AUTOINCREMENT,
  title varchar not null,
  first_name varchar not null,
  middle_name varchar,
  last_name varchar not null,
  street varchar,
  city varchar ,
  state varchar ,
  country varchar ,
  birth_date date not null,
  email varchar not null,
  password varchar not null
);

create table student_academic_details(
  id integer primary key AUTOINCREMENT,
  degree varchar not null,
  major varchar,
  semester integer not null
);


create table majors_lookup (
  id integer primary key AUTOINCREMENT,
  major_code varchar not null,
  major_name varchar not null,
  add_column1 varchar ,
  add_column2 varchar
  );

create table course_lookup (
  id integer primary key AUTOINCREMENT,
  course_code varchar not null,
  course_name varchar not null,
  major_code varchar,
  course_rating integer,
  prerequisite VARCHAR,
  credits integer not null,
  description VARCHAR
  );

