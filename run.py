# all the imports
import sqlite3
import my_config
import sys
from flask import Flask, request, session, g, redirect, url_for, \
     abort, render_template, flash
from contextlib import closing
from database import db_session
from dbmodel import User
from send_email import send_email_for_confirm
import time
from limit_func import check_the_email, check_the_password

app = Flask(__name__)
app.config.from_object(my_config)


@app.route('/')
def index():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
    flash('You were logged in')
    return render_template('layout.html')


@app.route('/signin', methods=['GET', 'POST'])
def signin():
    error = None
    if request.method == 'POST':
        email = request.form['email']
        name = request.form['name']
        password = request.form['password']
        password1 = request.form['password1']
        if (password != password1):
            flash('两次输入的密码不一致')
            return render_template('signin.html')
        if not check_the_password(password):
            flash('密码不符合要求,密码长度应该在4到25之间并不能仅为数字')
            return render_template('signin.html')
        if not check_the_email(email):
            flash('邮箱格式错误')
            return render_template('signin.html')
        check_email = User.query.filter(User.email == email).first()
        if check_email:
            flash('邮箱已被注册>_<')
        else:
            flash('已经发送邮件到你的邮箱,请立刻激活帐号')
            new_user = User(name, email, password)

            session['unconfirm'] = True
            session['user_email'] = new_user.email

            db_session.add(new_user)
            db_session.commit()
            """
            send_email_for_confirm(email, new_user.email, new_user.reg_time,
                                   new_user.confirm)

            """
            return redirect(url_for('signined'))
    return render_template('signin.html')


@app.route('/signined/', methods=['POST', 'GET'])
def signined():
    if not session.get('unconfirm'):
        return redirect(url_for('login'))
    error = None
    if request.method == 'POST' and request.form.get('send_email_again'):
        new_user = User.query.filter(
            User.email == session['user_email']).first()
        if not new_user:
            return redirect(url_for('login'))

        if session.get('click_button_time'):
            session['click_button_time'] = session['click_button_time'] + 1
        else:
            session['click_button_time'] = 1
        if session['click_button_time'] > 5:
            flash('点击次数过多')
            session['click_button_time'] = 0
            session.pop('click_button_time', None)
            session.pop('unconfirm', None)
            return redirect(url_for('login'))

        #send_email_for_confirm(new_user.email, new_user.email,
        #                       new_user.reg_time, new_user.confirm)

        flash('再次发送邮件')
    return render_template('signined.html')


@app.route('/confirm/<email>/<reg_time>/<confirm>')
def confirm(email, reg_time, confirm):
    error = None
    check_email = User.query.filter(User.email == email
                                    and User.confirm == confirm).first()
    if check_email:
        if str(check_email.reg_time) == reg_time:
            nowtime = int(time.time())
            if (nowtime - int(reg_time) > 3600):
                flash('验证时间太晚')
                session.pop('unconfirm', None)
                session.pop('click_button_time', None)
                return render_template('login.html')
            session['logged_in'] = True
            session.pop('unconfirm', None)
            session.pop('click_button_time', None)
            check_email.confirm = 0
            db_session.commit()
            flash('You were logged in')
            return render_template('layout.html')
    return render_template('login.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':

        user_email = request.form['user_email']
        password = request.form['password']

        if request.form.get('reset_password'):
            print("try to reset_password")
            U = User.query.filter(User.email == user_email).first()
            if not U:
                flash('该邮箱未被注册....')
                return render_template('login.html')
            pass
            
        U = User.query.filter(User.email == user_email).first()
        if U:
            if U.judge_password(password):
                if U.confirm == 0:
                    session['logged_in'] = True
                    return redirect(url_for('index'))
                else:
                    flash('未验证邮箱')
                    return render_template('login.html')
            else:
                flash('wrong password!')
                return render_template('login.html')
        else:
            flash('该邮箱未被注册....')
    return render_template('login.html')


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('login'))


@app.before_request
def before_request():
    pass


@app.teardown_request
def teardown_request(exception):
    db_session.remove()


@app.errorhandler(404)
def page_not_found(error):
    return render_template('page_not_found.html'), 404


if __name__ == '__main__':
    if my_config.clear_all_database:
        from database import init_db
        init_db()
    app.run(host='0.0.0.0', port=my_config.port)
