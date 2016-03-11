import sys
import json
import datetime
from datetime import timedelta

from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import url_for
from flask import redirect
from flask import session

sys.path.append('..')

from _models.util.get_text  import *
from _models.differ.diffmain  import *
from _models.util.easyLog import *
#from _models.util.mail import *
import _models.util

from _config.database import *
from _config import checker
import _config.hash


app = Flask(__name__)

app.permanent_session_lifetime = timedelta(minutes=2**12)

app.secret_key = _config.hash.flask_secret_key


@app.route('/signin',methods=['GET','POST'])
def signin():

    next_ = request.args.get('next',None)
    if not session.get('login',False):
        if request.method=='GET':
            return render_template('signin.html')
        elif request.method=='POST':
            if request.form.get('email','')=='':
                flash('Please enter email','danger')
                return redirect(url_for('signin'))
            elif not checker.mail(request.form.get('email','')):
                flash('Illegal email','danger')
                return redirect(url_for('signin'))
            else:
                email = request.form.get('email','')

            if request.form.get('password','')=='':
                flash('Please enter password','danger')
                return redirect(url_for('signin'))
            elif not checker.password(request.form.get('password','')):
                flash('Illegal password','danger')
                return redirect(url_for('signin'))
            else:
                password = request.form.get('password','')

            remember = request.form.get('remember',False)
            if remember:
                session.permanent = True
            else:
                pass

            salt = _config.hash.salt
            user_info = User.select().where(User.mail==email)
            if len(user_info)==0:
                new_user = User(mail=email,password=_config.hash.uhash(password,salt))
                new_user.save()
                user_info = User.select().where(User.mail==email)
            verify = False
            for user in user_info:
                if _config.hash.uhash(password,salt)==user.password:
                    verify = True
                    session['login'] = True
                    session['uid'] = user.id
            if verify:
                if next_:
                    response = Response()
                    response.set_cookie('expires','False',expires= expires)
                    return redirect(url_for(next_))
                else:
                    return redirect(url_for('dashboard'))
            else:
                flash('Verify fail','danger')
                return redirect(url_for('signin'))
    else:
        if next_:
            return redirect(url_for(next_))
        else:
            return redirect(url_for('dashboard'))

@app.route('/dashboard/addpage')
def addpage():
    uid = session['uid']
    mail = User.select().where(User.id==uid)[0].mail
    return render_template('addpage.html',mail=mail,username=mail)

@app.route('/dashboard/del')
def del_():
    next_ = request.args.get('next','dashboard')
    uid = session['uid']
    mail = User.select().where(User.id==uid)[0].mail
    tid = request.args.get('id',None)
    user_info = User.select().where(User.id==uid)[0]
    sideload = json.loads(user_info.sideload)
    sideload['tasks'].remove(int(tid))
    user_info.sideload = json.dumps(sideload)
    user_info.save()
    #band = Artist.get(Artist.name=="MXPX")
    #band.delete_instance()
    task = Task.select().where(Task.id==tid)[0]
    task.delete_instance()
    flash('Item deleted.','success')
    if next_:
        return redirect(url_for(next_))
    else:
        return redirect(url_for('dashboard'))

@app.route('/add',methods=['GET'])
def add():
    next_ = request.args.get('next',None)
    url = request.args.get('url',None)
    mail = request.args.get('mail',None)
    if _models.util.check_url(url) and checker.mail(mail):
        url = _models.util.true_url(url)
        task = Task.select().where(Task.url==url)
        if len(task)>0:
            task = task[0]
            new_mail_task = MailTask(   expired=datetime.datetime.now()+datetime.timedelta(seconds=60*60*24*30),\
                                        tid=task.id,\
                                        mail=mail,\
                                        last_update=datetime.datetime.now(),\
                                        every=60*60*24,\
                                        template='moniter')
            new_mail_task.save()
            if session.get('login',False):
                uid = session['uid']
                user_info_ = User.select().where(User.id==uid)
                user_info = user_info_[0]#
                if user_info.sideload==None:
                    sideload=json.dumps({'tasks':[task.id]})
                    user_info.sideload=sideload
                    user_info.save()
                    flash('You will receive the mail about the changing of the url.','success')
                    if next_:
                        return redirect(url_for(next_))
                    else:
                        return redirect(url_for('index'))
                else:
                    obj = json.loads(user_info.sideload)
                    obj['tasks'].append(task.id)
                    user_info.sideload=json.dumps(obj)
                    user_info.save()
                    if task.id not in obj['tasks']:
                        obj['tasks'].append(task.id)
                        flash('You will receive the mail about the changing of the url.','success')
                        if next_:
                            return redirect(url_for(next_))
                        else:
                            return redirect(url_for('index'))
                    else:
                        flash('Please not add this again.','warning')
                        if next_:
                            return redirect(url_for(next_))
                        else:
                            return redirect(url_for('index'))
            else:
                flash('You will receive the mail about the changing of the url in next one month.','success')
                if next_:
                    return redirect(url_for(next_))
                else:
                    return redirect(url_for('index'))
        else:
            if session.get('login',False):
                uid = session['uid']
                user_info = User.select().where(User.id==uid)
                new_task = Task(uid=uid,url=url,slot='12H',)
                new_task.save()
                mail = User.select().where(User.id==uid)[0].mail
                new_mail_task = MailTask(   expired=datetime.datetime.now()+datetime.timedelta(seconds=60*60*24*30),\
                                            mail=mail,\
                                            last_update=datetime.datetime.now(),\
                                            every=60*60*60*24,\
                                            template='moniter')
                new_mail_task.save()
                flash('You will receive the mail about the changing of the url.','success')
                if next_:
                    return redirect(url_for(next_))
                else:
                    return redirect(url_for('index'))
            else:
                new_task = Task(uid=-1,url=url,slot='12H',)
                new_task.save()
                tid = Task.select().order_by(Task.id.desc()).limit(1)[0].id
                new_mail_task = MailTask(   expired=datetime.datetime.now()+datetime.timedelta(seconds=60*60*24*30),\
                                            tid=tid,\
                                            mail=mail,\
                                            last_update=datetime.datetime.now(),\
                                            every=60*60*60*24,\
                                            template='moniter')
                new_mail_task.save()
                flash('You will receive the mail about the changing of the url.','success')
                if next_:
                    return redirect(url_for(next_))
                else:
                    return redirect(url_for('index'))

@app.route('/dashboard/detail')
def detail():
    next_ = request.args.get('next','dashboard')
    uid = session['uid']
    mail = User.select().where(User.id==uid)[0].mail
    tid = request.args.get('id',None)
    last_content = Pool.select().where(Pool.tid==tid).order_by(Pool.time.desc()).limit(2)
    if len(last_content)==2:
        if old_content==new_content:
            flash('No changes','success')
            return render_template('detail.html')
        else:
            old_content = last_content[1].data
            new_content = last_content[0].data
            old_list = get_text(old_content)
            new_list = get_text(new_content)
            words1,words2 = filer(old_list,new_list)
            time0 = str(last_content[0].time)
            time1 = str(last_content[2].time)
            return render_template('detail.html',time0=time0,time1=time1,words1=words1,words2=words2)
    else:
        flash('No changes','success')
        return render_template('detail.html')

@app.route('/recovery',methods=['GET'])
def recovery():
    return '405 - Not support'
    
@app.route('/dashboard',methods=['GET'])
def dashboard():
    next_ = request.args.get('next',None)
    if not session.get('login',False):
        flash('Please login.','danger')
        if next_:
            return redirect(url_for(next_))
        else:
            return redirect(url_for('signin'))
    else:
        uid = session['uid']
        user_info = User.select().where(User.id==uid)[0]
        if user_info.sideload==None:
            table = []
        else:
            user_data = json.loads(user_info.sideload)
            tasks = user_data.get('tasks',[])
            table = []
            for task in tasks:
                task_info = Task.select().where(Task.id==task)
                for item in task_info:
                    if item.news==None:
                        item.news=''
                    else:
                        item.news=' ! '
                    if item.last_update==None:
                        item.last_update==''
                    table.append(
                            {
                                'id':task,
                                'url':item.url,
                                'last_update':item.last_update,
                                'frequency':item.slot,
                                'news':item.news
                            }
                        )
        return render_template('dashboard.html',username=user_info.mail,tasks=table)

@app.route('/',methods=['GET','POST'])
def index():

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=1)