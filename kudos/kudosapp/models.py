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

class Employee(models.Model):
    dept = models.CharField(max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    location = models.CharField(max_length=100, null=True)

    def get_image_file(self):
        return self.first_name.lower() + '_' + self.last_name.lower() + '.jpg'

    def image_exists(self):
        import os
        file = '/var/www/TMKudos/kudos/kudosapp/static/images/profiles/'+self.get_image_file()
        return file;

    def hashcode(self):
        import md5
        hashm=md5.new(self.first_name)
        return hashm.hexdigest()

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def __unicode__(self):
        return self.get_full_name()

class Kudos(models.Model):
    from_employee = models.ForeignKey('employee', related_name='sent_kudos')
    to_employee = models.ForeignKey('employee', related_name='received_kudos')
    created = models.DateTimeField(default=datetime.datetime.now())
    subject = models.CharField(max_length=511)
    body = models.TextField()
    flagged = models.BooleanField(default=False)
    tags = models.CharField(max_length=50, null=True, blank=True)
    message_id = models.CharField(max_length=255, null=True, blank=True)

    def get_delimited_tags(self):
        tags = self.tags[:-1].split(',')
        return tags

    @property
    def get_from_employee_sent_kudos_count(self):
        return self.from_employee.sent_kudos.count()

    @property
    def get_to_employee_sent_kudos_count(self):
        return self.to_employee.sent_kudos.count()

    @property
    def get_from_employee_received_kudos_count(self):
        return self.from_employee.received_kudos.count()

    @property
    def get_to_employee_received_kudos_count(self):
        return self.from_employee.received_kudos.count()

    def __unicode__(self):
        return self.subject

