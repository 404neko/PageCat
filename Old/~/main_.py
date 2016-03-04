from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash, _app_ctx_stack

import MySQLdb

import config.database
from config.salt import *
import config.checker
from config.hash import *

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

@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        def check_ip(ip):
            return True
        ip = request.remote_addr
        username = request.form.get('username','username_')
        password = request.form.get('username','password_')
        if config.checker.username(username) and config.checker.password(password) and username!='username_' and password!='password_' and check_ip(ip):
            hash_password = uhash(password,SALT_PASSWORD)
            connect = get_database()
            cursor = connect.cursor()
            try:
                cursor.execute('SELECT password FROM `fetch`.`user` WHERE username=\'%s\''%(username,))
            except:
                return render_template('info.html',error='error')
            if password==hash(credential['password'],salt):
                token = hash(credential['username']+credential['ip']+str(time.time()))
                cursor.execute('INSERT INTO `fetch`.`stage` (`username`, `ip`, `token`) VALUES (\'%s\', \'%s\', \'%s\');'%(credential['username'],credential['ip'],token,))
                connect.commit()
                #@setcookie 
                return render_template('info.html',error='error')
            else:
                return render_template('info.html',error='pw error')
        else:
            return render_template('info.html',error='feifa')

@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    else:
        def check_ip(ip):
            return True
        ip = request.remote_addr
        username = request.form.get('username','username_')
        password = request.form.get('username','password_')
        mail = request.form.get('mail','mail_')
        if config.checker.username(username) and config.checker.password(password) and config.checker.mail(mail) and username!='username_' and password!='password_' and mail!='mail_' and check_ip(ip):
            
            hash_password = uhash(password,SALT_PASSWORD)
            connect = get_database()
            cursor = connect.cursor()
    hash_password = uhash(credential['password'],salt)
    connect = database
    cursor = connect.cursor()
    try:
        cursor.execute('INSERT INTO `fetch`.`user` (`username`, `mail`, `password`) VALUES (\'%s\', \'%s\', \'%s\');'%(credential['username'],credential['mail'],hash_password,))
    except:
        return {'stage':'error','key':'execute','info':''}
    connect.commit()
    return {'stage':'success','key':'','info':''}


@app.route('/')
def index():
    get_database()
    return 'Nyan~'

if __name__ == '__main__':
    app.run(debug=True)