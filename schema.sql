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

insert into majors_lookup(major_code,major_name) values ("INFM","Information Management");
insert into majors_lookup(major_code,major_name) values ("CMSC","Computer Science");
insert into majors_lookup(major_code,major_name) values ("ENTS","Telecommunication");
insert into majors_lookup(major_code,major_name) values ("ENEE","Electrical and Computer Engineering");



insert into student_account_details(title,first_name,middle_name,last_name,email,birth_date,password) values ("Miss","Prajakta","Sanjeev","Arolker","admin","24-AUG-1990","admin");


insert into student_academic_details(degree,major,semester) values ("Masters","Information Management","Fall 2014");

insert into student_course_details(id, course_name, course_code, semester) values (1,"INFM600 - Information Environments","INFM600","Fall 2014");
insert into student_course_details(id, course_name, course_code, semester) values (1,"INFM603 - Information Technology","INFM603","Fall 2014");

insert into student_interests(s_id, tag_name) VALUES (1,"programming");
insert into student_interests(s_id, tag_name) VALUES (1,"web development");

select c.course_code from course_lookup c where c.course_code in (
  SELECT t.course_code from course_tags t where t.tag_name IN (
  SELECT s.tag_name from student_interests s where s.s_id = 1)
) and c.course_code not in (SELECT cc.course_code from student_course_details cc where cc.id = 1);


-- //INFM
insert into course_lookup(course_code,course_name,major_code,course_rating,credits,prerequisite,description) values ("INFM600","INFM600 - Information Environments","INFM",1,3,"None","Role and function of information in organizations. Organizational environment and its influence on internal and external communication, organizational structure and management, organizational culture, information flow, organizational identity. Shared mental models and group decision ma king. Differences among types of organizations. Information policy.");
insert into course_lookup(course_code,course_name,major_code,course_rating,credits,prerequisite,description) values ("INFM603","INFM603 - Information Technology and Organizational Context","INFM",2,3,"None","Application of communication and information technologies to support work processes, including technology-enhanced communication networks, computer-supported collaborative work, decision-support systems, interactive systems, and systems analysis. Acquisition of information systems and their integration into the organization.");
insert into course_lookup(course_code,course_name,major_code,course_rating,credits,prerequisite,description) values ("INFM605","INFM605 - Users and Use Context","INFM",4,3,"None","Use of information by individuals. Nature of information. Information behavior and mental models. Characteristics of problems, task analysis, problem solving, and decision making. Methods for determining information behavior and user needs. Information access. Information technology as a tool in information use.");
insert into course_lookup(course_code,course_name,major_code,course_rating,credits,prerequisite,description) values ("INFM612","INFM612 - Management of Information Program and Services","INFM",5,3,"None","Administration of information programs, services, and projects, including the role of leadership in management; developing mission, vision, and goals; providing effective management for results; managing professionals; financial management; and professional conduct and ethical issues.");
insert into course_lookup(course_code,course_name,major_code,course_rating,credits,prerequisite,description) values ("INFM620","INFM620 - Introduction to Strategic Informatino Management","INFM",2,3,"INFM612","Defining and identifying strategic information in an organization. Characteristics of strategic information management, including the principles, practices, issues, and programs involved with the strategic management and protection of information in organizations.");
insert into course_lookup(course_code,course_name,major_code,course_rating,credits,prerequisite,description) values ("INFM700","INFM700 - Information Technology and Organizational Context","INFM",4,3,"INFM603","Principles and techniques of information organization and architecture for the Web environment. Structured description of digital resources, including data modeling techniques, metadata schemes, and user-oriented navigation systems.");
insert into course_lookup(course_code,course_name,major_code,course_rating,credits,prerequisite,description) values ("INFM711","INFM711 - Financial Management of Information Projects","INFM",1,3,"None","Techniques and strategies of planning and executing successful projects Project budgets, work breakdown structures and scheduling techniques, earned value, tracking and reporting project costs, risk management, best practices, and cost/benefit analysis");
insert into course_lookup(course_code,course_name,major_code,course_rating,credits,prerequisite,description) values ("INFM714","INFM714 - Principles of Competitive Intelligence","INFM",1,3,"None","Intelligence process and how to build business advantage by the collection and analysis of the capabilities, vulnerabilities, market positioning and strategic planning of competitors using open source information.");
insert into course_lookup(course_code,course_name,major_code,course_rating,credits,prerequisite,description) values ("INFM732","INFM732 - Information Audits and Environmental Scans","INFM",1,3,"INFM600","Techniques to assess the information needs of an organization to meet its strategic objectives. Methods of identifying information sources and gaps and of scanning the internal and external environment to identify changes that affect the organization. Application of information audits and environmental scans in strategic information management.");
insert into course_lookup(course_code,course_name,major_code,course_rating,credits,prerequisite,description) values ("INFM743","INFM743 - Development of Internet Applications","INFM",1,3,"INFM603","Mark up languages and methods for manipulating marked-up content. Techniques for adding interactivity to web pages. Installing and running servers. Server-side applications. Application programming interfaces for third-party content and tools. Extension development.");
insert into course_lookup(course_code,course_name,major_code,course_rating,credits,prerequisite,description) values ("INFM750","INFM750 - From Data to Insights","INFM",1,3,"INFM603 and INST737","Application of data science techniques to unstructured, real-world datasets including social media and geo-referenced sources. Techniques and approaches to extract information relevant for experts and non-experts in areas that include smart cities, public health, and disaster management");



/*
Programming
Web Development
Data Analytics
Strategic Management
Database
Information Systems*/

insert into course_tags(course_code, tag_name) VALUES ("INFM600","core");
insert into course_tags(course_code, tag_name) VALUES ("INFM603","core");
insert into course_tags(course_code, tag_name) VALUES ("INFM605","core");
insert into course_tags(course_code, tag_name) VALUES ("INFM612","core");

insert into course_tags(course_code, tag_name) VALUES ("INFM612","strategic management");
insert into course_tags(course_code, tag_name) VALUES ("INFM620","strategic management");
insert into course_tags(course_code, tag_name) VALUES ("INFM700","web development");
insert into course_tags(course_code, tag_name) VALUES ("INFM714","strategic management");
insert into course_tags(course_code, tag_name) VALUES ("INFM743","programming");
insert into course_tags(course_code, tag_name) VALUES ("INFM743","python");
insert into course_tags(course_code, tag_name) VALUES ("INFM750","data analytics");

-- //INST
insert into course_lookup(course_code,course_name,major_code,course_rating,credits,prerequisite,description) values ("INST603","INST603 - Systems Analysis and Design","INST",1,3,"None","Formal process for planning and designing an information technology system, including identifying users and other stakeholders, analyzing work processes, preparing system specifications, conducting feasibility and usability studies, and preparing for implementation. Approaches to analyzing system components and functions. Measurement and evaluation of system performance.");
insert into course_lookup(course_code,course_name,major_code,course_rating,credits,prerequisite,description) values ("INST610","INST610 - Information Ethics","INST",1,3,"None","Investigation of the diverse range of ehtical challanges facing society in the information age. Ethical theories, including non-Western and feminist theories. Application of theories to information ethics issues.");
insert into course_lookup(course_code,course_name,major_code,course_rating,credits,prerequisite,description) values ("INST613","INST613 - Information and Human Rights","INST",1,3,"None","An examination of information as a human right, including topics: social, cultural, economic, legal, and political forces shaping information rights; the impact of information rights on information professions, standards, and cultural institutions; and information rights and disadvantaged populations.");
insert into course_lookup(course_code,course_name,major_code,course_rating,credits,prerequisite,description) values ("INST630","INST630 - Introduction to Programming for the Information Professional","INST",1,3,"None","An introduction to computer programming intended for students with no previous programming experience. Topics include fundamentals of programming and current trends in user interface implementation that are relevant to information professionals.");
insert into course_lookup(course_code,course_name,major_code,course_rating,credits,prerequisite,description) values ("INST632","INST632 - Human-Computer Interaction Design Methods","INST",1,3,"None","Methods of user-centered design, including task analysis, low-tech prototyping, user interviews, usability testing, participatory design, and focus groups");
insert into course_lookup(course_code,course_name,major_code,course_rating,credits,prerequisite,description) values ("INST640","INST640 - Principles of Digital Curation","INST",1,3,"None","Principles for the design and implementation of long-term curation of digital data and information assets, including born-digital and digitized assets. Frameworks for analysis of technical, practical, economic, legal, social and political factors affecting digital curation decisions. Case studies of specific digital curation scenarios.");
insert into course_lookup(course_code,course_name,major_code,course_rating,credits,prerequisite,description) values ("INST706","INST706 - Project Management","INST",1,3,"INFM603 and INFM612","Comprehensive overview of project management, focusing on the needs of information resource (IR) projects. Concepts and techniques for planning and execution of projects including developing work breakdown structure, estimating costs, managing risks, scheduling, staff and resource allocation, team building, communication, monitoring, control, and other aspects of successful project completion");
insert into course_lookup(course_code,course_name,major_code,course_rating,credits,prerequisite,description) values ("INST714","INST714 - Information for Decision-Making","INST",1,3,"None","The use of information in organizational and individual decision-making Managers' behavior in using information, differences between the private and public sectors, and the roles of information professionals and information systems in decision-making.");
insert into course_lookup(course_code,course_name,major_code,course_rating,credits,prerequisite,description) values ("INST734","INST734 - Information Retrieval Systems","INST",1,3,"INFM603","Principles of organizing and providing access to information using automated information storage and retrieval systems. Retrieval systems models, index language selection, data structure, user interfaces, and evaluation for text and multimedia applications.");
insert into course_lookup(course_code,course_name,major_code,course_rating,credits,prerequisite,description) values ("INST733","INST733 - Database Design","INST",1,3,"None","Principles of organizing and providing access to information using automated information storage and retrieval systems. Retrieval systems models, index language selection, data structure, user interfaces, and evaluation for text and multimedia applications.");
insert into course_lookup(course_code,course_name,major_code,course_rating,credits,prerequisite,description) values ("INST737","INST737 - Digging Into Data","INST",1,3,"INFM603","An exploration of some of the best and most general approaches to get the most information out of data through clustering, classification, and regression techniques.");


insert into course_tags(course_code, tag_name) VALUES ("INST603","information systems");
insert into course_tags(course_code, tag_name) VALUES ("INST610","information policy");
insert into course_tags(course_code, tag_name) VALUES ("INST613","information policy");
insert into course_tags(course_code, tag_name) VALUES ("INST630","programming");
insert into course_tags(course_code, tag_name) VALUES ("INST632","strategic management");
insert into course_tags(course_code, tag_name) VALUES ("INST640","digital curation");
insert into course_tags(course_code, tag_name) VALUES ("INST706","strategic management");
insert into course_tags(course_code, tag_name) VALUES ("INST714","data analytics");
insert into course_tags(course_code, tag_name) VALUES ("INST734","information systems");
insert into course_tags(course_code, tag_name) VALUES ("INST733","database");
insert into course_tags(course_code, tag_name) VALUES ("INST737","data analytics");

select cc.course_code,cc.course_name,cc.prerequisite from course_lookup cc,course_tags tt where cc.course_code = tt.course_code and tt.tag_name in (select t.tag_name from course_tags t where t.course_code in (SELECT c.course_code from student_course_details c where c.id = 1)) and cc.course_code not in (SELECT c.course_code from student_course_details c where c.id = 1);