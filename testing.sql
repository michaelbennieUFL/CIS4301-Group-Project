

-- create the tables

drop table MICHAELBENNIE.STUDENT;

CREATE TABLE student(
    student_id INT,
    name       varchar2(30),
    major      varchar2(20),
    primary key (student_id)
);

Alter table MICHAELBENNIE.STUDENT add gpa decimal(3,2);


alter table MICHAELBENNIE.STUDENT drop column gpa;

insert into MICHAELBENNIE.STUDENT values (1,'小賀','電腦科學');

insert into MICHAELBENNIE.STUDENT values (2,'小綠',NULL);


select * from MICHAELBENNIE.STUDENT;
