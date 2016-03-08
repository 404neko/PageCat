from peewee import *

database = MySQLDatabase('fetch', **{'host': '106.185.40.164', 'password': 'AlexprprHaoqiao', 'port': 3306, 'user': 'root'})

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
    sideload = TextField(null=False)

    class Meta:
        db_table = 'user'

class Task(BaseModel):

    tid = IntegerField(null=False)
    uid = IntegerField(null=False)
    url = TextField(null=False)
    last_update = DateTimeField(null=False)
    slot = CharField(null=False)
    news = TextField(null=True)

if __name__ == '__main__':
    Pool.create_table(True)
    User.create_table(True)
    Task.create_table(True)