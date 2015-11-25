from flask import render_template, request, redirect, url_for, flash
from flask.ext.login import login_required, login_user, logout_user, current_user
from flask_pymongo import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

from forms import *
from models import User
from pyblog import app, mongo, login_manager


@app.route('/')
def index():
    user = getMe()
    blogCollection = mongo.db.blogs.find({'userId': ObjectId(user.get_id())})
    blogs = list(blogCollection)
    for blog in blogs:
        blog.setdefault('user', user)
    print(blogs)
    return render_template('index.html', blogs=blogs)


@app.route('/blog/<id>')
def viewBlog(id):
    blog = mongo.db.blogs.find_one_or_404({'_id': ObjectId(id)})
    blog.setdefault('user', getMe())
    return render_template('blog.html', blog=blog)


@app.route('/postBlog', methods=['GET', 'POST'])
@login_required
def postBlog():
    form = PostForm()
    if form.validate_on_submit():
        blog = form.getBlog()
        blog["userId"] = ObjectId(current_user.get_id())
        mongo.db.blogs.insert(blog)
        flash('发布成功')
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('post.html', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = mongo.db.users.find_one({'userName': form.userName.data})
        if user is not None and check_password_hash(user['password'], form.password.data):
            login_user(User(user), form.rememberMe.data)
            return redirect(request.args.get('next') or url_for('index'))
        flash('用户名或密码错误')
    return render_template('login.html', form=form)


@login_manager.user_loader
def load_user(user_id):
    me = mongo.db.users.find_one({'_id': ObjectId(user_id)})
    if me:
        return User(me)
    else:
        return None


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('您已经退出登录')
    return redirect(url_for('index'))


@app.route('/about')
def about():
    return render_template('about.html')


@app.before_first_request
def initMe():
    me = mongo.db.users.find_one({'userName': 'hym'})
    if not me:
        mongo.db.users.insert({'userName': 'hym', 'password': generate_password_hash('123456'), 'nickName': '星奕'})


def getMe():
    me = mongo.db.users.find_one({'userName': 'hym'})
    if me:
        return User(me)
    else:
        initMe()
        return getMe()
