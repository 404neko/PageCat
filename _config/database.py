from peewee import *

from connect import *

class BaseModel(Model):

    class Meta:
        database = database

class Pool(BaseModel):

    data = TextField(null=False)
    time = DateTimeField(null=False)
    tid = IntegerField(null=False)
    #did = CharField(null=False)

    class Meta:
        db_table = 'pool'

class User(BaseModel):

    username = CharField(null=True)
    password = CharField(null=False)
    mail = CharField(null=False)
    #uid = CharField(null=False) //use id
    sideload = TextField(null=True)

    class Meta:
        db_table = 'user'

class Task(BaseModel):

    #id = IntegerField(null=False)//use id
    uid = IntegerField(null=False)
    url = TextField(null=False)
    last_update = DateTimeField(null=True)
    slot = CharField(null=False)
    news = TextField(null=True)

    class Meta:
        db_table = 'task'

class MailQueue(BaseModel):
    time = DateTimeField(null=False)
    subject = TextField(null=False)
    msg = TextField(null=False)
    to = CharField(null=False)

    class Meta:
        db_table = 'mailqueue'

class MailTask(BaseModel):

    expired = DateTimeField(null=False)
    tid = IntegerField(null=False)
    mail = CharField(null=False)
    every = IntegerField(null=False)
    template = CharField(null=False)

    class Meta:
        db_table = 'mailtask'

if __name__ == '__main__':
    Pool.create_table(True)
    User.create_table(True)
    Task.create_table(True)
    MailQueue.create_table(True)
    MailTask.create_table(True)