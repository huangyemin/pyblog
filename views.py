import datetime

from flask import render_template, request, redirect, url_for, flash
from flask.ext.login import login_required, login_user, logout_user

from forms import LoginForm
from models import User
from pyblog import app, mongo, login_manager


@app.route('/')
def index():
    if app.debug:
        blogs = [{'id': '1', 'title': '创新', 'postTime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                  'author': '星奕',
                  'summary': '创新创新创新创新创新创新创新'},
                 {'id': '2', 'title': '教育', 'postTime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                  'author': '星奕',
                  'summary': '教育教育教育教育教育教育教育教育'},
                 {'id': '3', 'title': '科技', 'postTime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                  'author': '星奕',
                  'summary': '科技科技科技科技科技科技科技'}]
    else:
        blogs = mongo.db.blogs.find()
    return render_template('index.html', blogs=blogs)


@app.route('/blog/<int:id>')
def viewBlog(id):
    if app.debug:
        blog = {'title': '创新', 'postTime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'author': '星奕',
                'summary': '创新创新创新创新创新创新创新',
                'content': '创新创新创新创新创新创新创新创新创新创新创新创新创新创新创新创新创新创新创新创新创新创新创新创新创新创新创新创新创新创新创新创新创新创新创新'}
    else:
        blog = mongo.db.blogs.find_one_or_404({'_id': id})
    return render_template('blog.html', blog=blog)


@app.route('/postBlog', methods=['GET', 'POST'])
@login_required
def postBlog():
    blog = request.json
    mongo.db.blogs.insert(blog)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User()
        if user is not None and user.password == form.password.data:
            login_user(user, form.rememberMe.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash('用户名或密码错误')
    return render_template('login.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    return User()


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经退出登录')
    return redirect(url_for('index'))


@app.route('/about')
def about():
    return render_template('about.html')
