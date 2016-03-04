from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, _app_ctx_stack

import MySQLdb

import config.database
from config.salt import *
import config.checker
from config.hash import *
from config.values import *

import requests

app = Flask(__name__)

def get_database():
    top = _app_ctx_stack.top
    if not hasattr(top, 'sql_database'):
        sql_database = MySQLdb.connect(config.database.database['host'],config.database.database['user'],config.database.database['password'],config.database.database['database'])
        top.sql_database = sql_database
    return top.sql_database

def init_database():
    with app.app_context():
        database = get_database()
        with app.open_resource('resource\schema.sql') as f:
            cursor = database.cursor()
            cursor.execute(f.read())
        database.commit()

@app.teardown_appcontext
def close_database_connection(exception):
    top = _app_ctx_stack.top
    if hasattr(top, 'sql_database'):
        top.sql_database.close()

@app.route('/')
def index():
    return render_template('index.html',Info = Info)

@app.router('/diff')
def diff():
    

@app.route('/create')
def create():
    url = request.args.get('url')
    email = request.args.get('email')
    if url==None:
        return render_template('index.html',Info = Info,Error = 'Please input url')
    elif email==None:
        return render_template('index.html',Info = Info,Error = 'Please input email')
    else:
        try:
            respon = requests.get(url)
        except:
           return render_template('index.html',Info = Info,Error = 'Can\'t open url: '+url)
    connect = get_database()
    cursor = connect.cursor()
    count = cursor.execute('SELECT * FROM `fetch`.`watcher` WHERE url=%s',(url,))
    print count
    if count==0:
        cursor.execute('INSERT INTO `fetch`.`watcher` (`url`,`slot`,`enabled`) VALUES (%s,%s,%s)',(url,'06H',1))
        connect.commit()
        print 1
    else:
        data = cursor.fetchall()
        if not data[0][-1]:
            cursor.execute('UPDATE `fetch`.`watcher` SET `enabled`=`1` WHERE `url`=%s',(data[0][0],))
    return render_template('index.html',Info = Info,)

if __name__ == '__main__':
    app.run(debug=True)