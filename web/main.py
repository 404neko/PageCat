import sys
import json
import datetime
from datetime import timedelta

import chardet

import html2text
from flask import Flask
from flask import render_template
from flask import request
from flask import flash
from flask import url_for
from flask import redirect
from flask import session

sys.path.append('..')

from _modules.util.get_text_  import *
from _modules.differ.diffmain  import *
from _modules.util.easyLog import *
#from _modules.util.mail import *
import _modules.util

from _config.database import *
from _config import checker
import _config.hash
import difflib

from _modules.differ.stromdiff import *

app = Flask(__name__)

app.permanent_session_lifetime = timedelta(minutes=2**12)

app.secret_key = _config.hash.flask_secret_key


@app.before_request
def _db_connect():
    database.connect()

@app.teardown_request
def _db_close(exc):
    if not database.is_closed():
        database.close()

@app.teardown_appcontext
def close_database(error):
    database.close()

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

@app.route('/dashboard/setting')
def setting():
    uid = session['uid']
    mail = User.select().where(User.id==uid)[0].mail
    return render_template('setting.html',mail=mail,username=mail)

@app.route('/dashboard/set')
def set():
    next_ = request.args.get('next','dashboard')
    every = request.args.get('frequency','1D')
    uid = session['uid']
    user_info = User.select().where(User.id==uid)[0]
    sideload = user_info.sideload
    if sideload not in ['(NULL)',None,'None','null']:
        json_ = json.loads(sideload)
        json_['every']=every
        user_info.sideload = json.dumps(json_)
        user_info.save()
    else:
        user_info.sideload = '{"every":"1D"}'
        user_info.save()
    flash('Saved.','success')
    if next_:
        return redirect(url_for(next_))
    else:
        return redirect(url_for('dashboard'))

@app.route('/dashboard/del')
def del_():
    next_ = request.args.get('next','dashboard')
    uid = session['uid']
    #mail = User.select().where(User.id==uid)[0].mail
    tid = request.args.get('id',None)
    user_info = User.select().where(User.id==uid)[0]
    sideload = json.loads(user_info.sideload)
    sideload['tasks'].remove(int(tid))
    user_info.sideload = json.dumps(sideload)
    user_info.save()
    #band = Artist.get(Artist.name=="MXPX")
    #band.delete_instance()
    task = Task.select().where(Task.id==tid)[0]
    task.active=0
    task.save()
    flash('Item deleted.','success')
    if next_:
        return redirect(url_for(next_))
    else:
        return redirect(url_for('dashboard'))

@app.route('/add_login',methods=['GET'])
def add_login():
    next_ = request.args.get('next','dashboard')
    url = request.args.get('url','')
    fetchf = request.args.get('fetchf','1D')
    if session.get('login',False):
        uid = session['uid']
        user_info = User.select().where(User.id==uid)
        mail = user_info[0].mail
        try:
            mailf = json.loads(user_info[0].sideload).get('every',86400)
        except:
            mailf = '1D'
        if _modules.util.check_url(url):
            url = _modules.util.true_url(url)
            exists_task = Task.select().where(Task.url==url)
            if len(exists_task)!=0:
                if mailf!='00':
                    tid = exists_task[0].id
                    exists_task[0].active=1
                    exists_task[0].save()
                    new_mail_task = MailTask(expired=datetime.datetime.now()+datetime.timedelta(seconds=60*60*24*2333),\
                                            tid=tid,\
                                            mail=mail,
                                            every=_modules.util.delay_cal(mailf),\
                                            template='moniter'
                                        )
                    new_mail_task.save()
                else:
                    pass
            else:
                fetchf_ = fetchf
                if fetchf=='00':
                    fetchf='1D'
                new_task = Task(
                        uid = uid,
                        url =url,
                        slot = fetchf,
                    )
                new_task.save()
                tid = Task.select().where(Task.url==url)[0].id
                if mailf=='00':
                    mailf='1D'
                    new_mail_task = MailTask(expired=datetime.datetime.now()+datetime.timedelta(seconds=60*60*24*365*99),\
                                            tid=tid,\
                                            mail=mail,
                                            every=_modules.util.delay_cal(mailf),\
                                            template='moniter'
                                        )
                    new_mail_task.save()
                else:
                    new_mail_task = MailTask(expired=datetime.datetime.now()+datetime.timedelta(seconds=60*60*24*365*99),\
                                            tid=tid,\
                                            mail=mail,
                                            every=_modules.util.delay_cal(mailf),\
                                            template='moniter'
                                        )
                    new_mail_task.save()
            if user_info[0].sideload in ['(NULL)',None,'None','null']:
                user_info[0].sideload = json.dumps({'tasks':[tid]})
                user_info[0].save()
            else:
                old_sideload = json.loads(user_info[0].sideload)
                if tid in old_sideload['tasks']:
                    flash('Url exists.','danger')
                    if next_:
                        return redirect(url_for(next_))
                    else:
                        return redirect(url_for('index'))
                else:
                    old_sideload['tasks'].append(tid)
                    user_info[0].sideload = json.dumps(old_sideload)
                    user_info[0].save()
            flash('You will receive the mail about the changing of the url.','success')
            if next_:
                return redirect(url_for(next_))
            else:
                return redirect(url_for('index'))


@app.route('/add_anonymous',methods=['GET'])
def add_anonymous():
    next_ = request.args.get('next','')
    url = request.args.get('url','')
    mail = request.args.get('mail','')
    if _modules.util.check_url(url):
        if checker.mail(mail):
            url = _modules.util.true_url(url)
            task = Task.select().where(Task.url==url)
            if len(task)>0:
                task = task[0]
                task.active = 1
                task.save()
                new_mail_task = MailTask(   expired=datetime.datetime.now()+datetime.timedelta(seconds=60*60*24*30),\
                                            tid=task.id,\
                                            mail=mail,\
                                            last_update=datetime.datetime.now(),\
                                            every=60*60*24,\
                                            template='moniter')
                new_mail_task.save()
                flash('You will receive the mail about the changing of the url in next one month.','success')
                if next_:
                    return redirect(url_for(next_))
                else:
                    return redirect(url_for('index'))
            else:
                new_task = Task(    uid = -1,
                                    url =url,
                                    slot = '1D',)
                new_task.save()
                tid = Task.select().where(Task.url==url)[0].id
                new_mail_task = MailTask(   expired=datetime.datetime.now()+datetime.timedelta(seconds=60*60*24*30),\
                                            tid=tid,\
                                            mail=mail,\
                                            last_update=datetime.datetime.now(),\
                                            every=60*60*24,\
                                            template='moniter')
                new_mail_task.save()
                flash('You will receive the mail about the changing of the url in next one month.','success')
                if next_:
                    return redirect(url_for(next_))
                else:
                    return redirect(url_for('index'))
        else:
            flash('Error mail address.','danger')
            if next_:
                return redirect(url_for(next_))
            else:
                return redirect(url_for('index'))
    else:
        flash('Error mail address.','danger')
        if next_:
            return redirect(url_for(next_))
        else:
            return redirect(url_for('index'))

@app.route('/add',methods=['GET'])
def add():
    next_ = request.args.get('next','')
    url = request.args.get('url','')
    mail = request.args.get('mail','')
    fetchf = request.args.get('fetchf','1D')
    if session.get('login',False):
        uid = session['uid']
        if url!='':
            return redirect(url_for('add_login')+'?url='+url+'&next='+next_+'&fetchf='+fetchf)
        else:
            flash('Please enter the url.','danger')
            return redirect(url_for('addpage'))
    else:
        if url!='':
            return redirect(url_for('add_anonymous')+'?url='+url+'&next='+next_+'&mail='+mail)
        else:
            flash('Please enter the url.','danger')
            return redirect(url_for('index'))

@app.route('/dashboard/detail')
def detail():
    next_ = request.args.get('next','dashboard')
    uid = session['uid']
    mail = User.select().where(User.id==uid)[0].mail
    tid = request.args.get('id',None)
    last_content = Pool.select().where(Pool.tid==tid).order_by(Pool.time.desc()).limit(2)
    if len(last_content)==2:
        old_content = last_content[1].data
        new_content = last_content[0].data
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
            time1 = str(last_content[1].time)
            return render_template('detail.html',time0=time0,time1=time1,words1=words1,words2=words2,mail=mail,username=mail)
    else:
        flash('No changes','success')
        return render_template('detail.html',mail=mail,username=mail)

@app.route('/dashboard/detail_')
def detail_():
    next_ = request.args.get('next','dashboard')
    uid = session['uid']
    mail = User.select().where(User.id==uid)[0].mail
    tid = request.args.get('id',None)
    last_content = Pool.select().where(Pool.tid==tid).order_by(Pool.time.desc()).limit(2)
    if len(last_content)==2:
        old_content = last_content[1].data
        new_content = last_content[0].data
        if old_content==new_content:
            flash('No changes','success')
            return render_template('detail.html')
        else:
            BASE_SITE = '<html><head>%s</head><body>%s</body></html>'
            #old_md = html2text.html2text(old_content.decode(chardet.detect(old_content)['encoding'],errors='ignore'))
            #new_md = html2text.html2text(new_content.decode(chardet.detect(new_content)['encoding'],errors='ignore'))
            old_md = html2text.html2text(old_content)
            new_md = html2text.html2text(new_content)
            l,r = strom(old_md,new_md)
            for i_ in l:
                print type(i_)
            nl,nr = c2html(l,r)
            return BASE_SITE % ('',nl+'\n'+nr)
    else:
        flash('No changes','success')
        return render_template('detail.html',mail=mail,username=mail)

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
            try:
                user_data = json.loads(user_info.sideload)
            except:
                user_data = {'tasks':[]}
            tasks = user_data.get('tasks',[])
            table = []
            for task in tasks:
                task_info = Task.select().where(Task.id==task)
                for item in task_info:
                    '''
                    if item.news==None:
                        item.news=''
                    else:
                        item.news=' ! '
                    '''
                    if item.last_update==None:
                        item.last_update==''
                    table.append(
                            {
                                'id':task,
                                'url':item.url,
                                'last_update':item.last_update,
                                'frequency':item.slot,
                                #'news':item.news
                            }
                        )
        return render_template('dashboard.html',username=user_info.mail,tasks=table)

@app.route('/',methods=['GET','POST'])
def index():

    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5001,host='0.0.0.0',debug=1)
