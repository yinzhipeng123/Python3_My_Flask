# -*- coding: utf-8 -*
import sqlite3


from flask import Flask, request, session, g, redirect, url_for, abort, render_template, flash
import datetime

import io
import configparser

from test.blue_test import blue_test



DATABASE = 'flaskr.db'
ENV = 'development'
DEBUG = True
SECRET_KEY = 'development key'



app = Flask(__name__)
app.register_blueprint(blue_test)
app.config.from_object(__name__)
app.app_context().push()


app.permanent_session_lifetime = datetime.timedelta(seconds=10*60)
#设置连接时长


def connect_db():
    return sqlite3.connect(app.config['DATABASE'])



@app.before_request
def before_request():
    g.db = connect_db()

@app.teardown_request
def teardown_request(exception):
    g.db.close()






@app.route('/')
def show_entries():
    username = session.get("logged_in")

    app.logger.debug("session===="+str(username))
    if username:
        useridcur = g.db.execute('select id  from users where user = ? ',[username]).fetchall()
        userid = int(useridcur[0][0])

        app.logger.debug("userid========"+str(userid))

        cur = g.db.execute('select title,text,id from entries where author = ?',[userid])
        entries = [dict(title=row[0], text=row[1],id=row[2]) for row in cur.fetchall()]
    else:
        entries=None
    return render_template('show_entries.html', entries=entries)

@app.route('/add', methods=['POST'])
def add_entry():
    if session.get('logged_in'):
        username = session.get("logged_in")
        useridcur = g.db.execute('select id  from users where user = ? ', [username]).fetchall()
        userid = int(useridcur[0][0])

        g.db.execute('insert into entries (id,title, text,author) values (?,?,?,?)', [None,request.form['title'], request.form['text'],userid])
        g.db.commit()
        flash('New entry was successfully posted')

    else:
        abort(401)
    return redirect(url_for('show_entries'))


@app.route('/register',methods=['GET','POST'])
def register():
    if request.method == 'POST':
        dbcur = g.db.execute('select * from users where user=?', [request.form['username']]).fetchall()

        if dbcur:
            flash('用户已经存在')
        else:
            g.db.execute('insert into users (id,user, password) values (?,?,?)',[None,request.form['username'], request.form['password']])
            g.db.commit()
            flash('注册成功')
    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        #根据用户名在数据库中查询
        dbcur=g.db.execute('select * from users where user=?',[request.form['username']]).fetchall()
        #如果查出的实例中有数据，则在判读密码是否相同，否则提示没有这个用户
        if dbcur:
            # if request.form['username'] != str(dbcur[0][1]):
            #     error = 'Invalid username'
            if request.form['password'] != str(dbcur[0][2]):
                error = '密码错误'
            else:
                session['logged_in'] = request.form['username']
                session.permanent = True
                flash('登录成功')

                return redirect(url_for('show_entries'))
        else:
            error = '沒有这个用户'
    return render_template('login.html', error=error)


@app.route('/<username>/<titleid>')
def titleid(username,titleid):   # 默认 id 为 None

    useridcur = g.db.execute('select id from users where user = ? ', [username]).fetchall()
    userid = int(useridcur[0][0])

    articlecur = g.db.execute('select title,text  from entries where id = ? and author=?',[titleid,userid]).fetchall()
    if articlecur:
        title=articlecur[0][0]
        text=articlecur[0][1]
    else:
        abort(401)
    return render_template('article.html', title=title,text=text)   # 将 id 参数传递到模板变量中










@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('你已经退出')
    return redirect(url_for('show_entries'))





@app.route('/synconfig',methods=['GET','POST'])
def synconfig():
    app.logger.debug("synconfig========")
    if request.method == 'POST':
        num="lianjie = "+request.form['connectnum']+"\n"
        mem="daxiao = "+request.form['mem']+"\n"
        fout = io.open('config.conf','w',encoding='utf8')
        fout.write(u"[mysql]\n")
        fout.write(num)
        fout.write(mem)
        fout.close()
        flash('同步配置成功')
    return render_template('config.html')





if __name__ == '__main__':
    #在服务器上，这么启动
    # app.run(host='0.0.0.0')
    app.run()
