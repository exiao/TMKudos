from django.db import models

import datetime

# Create your models here.
"""drop table if exists employees;
create table employees (
id int unsigned auto_increment primary key,
employee_id int,
first_name varchar(100) not null,
last_name varchar(100) not null,
email varchar(100) not null,
dept varchar(255) not null
)engine=innodb default charset=utf8;

drop table if exists kudos;
create table kudos (
from_employee int unsigned not null,
to_employee int unsigned not null,
created timestamp not null,
subject varchar(511),
body text
)engine=innodb default charset=utf8;"""

def employee(models.Model):
    EXEC = 'Executive'
    HR = 'Human Resources'
    APPENG = 'Application Engineering'
    OPS = 'Operations'
    UI = 'User Interface'
    RTB = 'RTB'
    ADOPS = 'Ad Operations'
    DEPT_CHOICES = (
        (EXEC ,'Executive'),
        (HR ,'Human Resources'),
        (APPENG ,'Application Engineering'),
        (OPS ,'Operations'),
        (UI ,'User Interface'),
        (RTB ,'RTB'),
        (ADOPS ,'Ad Operations'),
    )

    dept = models.CharField(choices=DEPT_CHOICES,
                              default=EXEC)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()

def kudos(models.Model):
    from_employee = models.ForeignKey("employee")
    to_employee = models.ForeignKey("employee")
    created = models.DateTimeField(default=datetime.datetime.now())
    subject = models.CharField(max_length=511)
    body = models.TextField()
