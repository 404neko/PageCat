import sys
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

from _config.database import *
from _config import checker
import _config.hash


app = Flask(__name__)

app.permanent_session_lifetime = timedelta(minutes=2**12)

app.secret_key = _config.hash.flask_secret_key


@app.route('/signin',methods=['GET','POST'])
def signin():

    next_ = request.args.get('next',None)
    print session.get('login',False)
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
                    return redirect(url_for('dash_board'))
            else:
                flash('Verify fail','danger')
                return redirect(url_for('signin'))
    else:
        if next_:
            return redirect(url_for(next_))
        else:
            return redirect(url_for('dash_board'))

@app.route('/add',methods=['GET'])
def recovery():
    return 'Nyan'

@app.route('/recovery',methods=['GET'])
def recovery():
    return 'Nyan'
    
@app.route('/dash_board',methods=['GET'])
def dash_board():
    return 'Nyan'


@app.route('/',methods=['GET','POST'])
def index():

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=1)