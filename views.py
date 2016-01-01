from flask import render_template, request, redirect, url_for, flash
from flask.ext.login import login_required, login_user, logout_user, current_user
from flask.ext.paginate import Pagination
from flask_pymongo import DESCENDING
from flask_pymongo import ObjectId
from werkzeug.security import generate_password_hash, check_password_hash

from forms import *
from manage import app
from models import User
from pyblog import mongo, login_manager


@app.route('/', defaults={'page': 1})
@app.route('/blogs/page/<int:page>')
def index(page):
    user = getMe()
    condition = {'userId': ObjectId(user.get_id())}
    db_blogs = mongo.db.blogs.find(condition).sort("postTime", DESCENDING)

    pageSize = app.config['PAGE_SIZE']
    skipNum = (page - 1) * pageSize
    blogCollection = db_blogs.skip(skipNum).limit(pageSize)
    blogs = list(blogCollection)
    for blog in blogs:
        blog.setdefault('user', user)
    pagination = Pagination(page=page, total=db_blogs.count(), per_page=pageSize, bs_version='3')
    return render_template('index.html', blogs=blogs, pagination=pagination)


@app.route('/blog/<id>')
def viewBlog(id):
    blog = mongo.db.blogs.find_one_or_404({'_id': ObjectId(id)})
    blog.setdefault('user', getMe())
    if not (current_user and current_user.is_authenticated):
        mongo.db.blogs.update({'_id': ObjectId(id)}, {'$inc': {'viewCount': 1}})
    return render_template('blog.html', blog=blog)


@app.route('/editBlog/<id>', methods=['GET', 'POST'])
@login_required
def editBlog(id):
    blog = mongo.db.blogs.find_one_or_404({'_id': ObjectId(id)})
    form = PostForm(data=blog)
    if form.validate_on_submit():
        formData = form.getBlog()
        formData.pop('postTime')
        mongo.db.blogs.update({'_id': ObjectId(id)}, {'$set': formData})
        flash('发布成功')
        return redirect(request.args.get('next') or url_for('index'))
    return render_template('post.html', form=form)


@app.route('/deleteBlog/<id>', methods=['GET', 'POST'])
@login_required
def deleteBlog(id):
    mongo.db.blogs.remove({'_id': ObjectId(id)})
    flash('删除成功')
    return redirect(request.args.get('next') or url_for('index'))

@app.route('/postBlog', methods=['GET', 'POST'])
@login_required
def postBlog():
    form = PostForm()
    if form.validate_on_submit():
        blog = form.getBlog()
        blog["userId"] = ObjectId(current_user.get_id())
        blog["viewCount"] = 0
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
    me = mongo.db.users.find_one({'userName': app.config['DEFAULT_USER']})
    if not me:
        mongo.db.users.insert(
            {'userName': app.config['DEFAULT_USER'], 'password': generate_password_hash(app.config['DEFAULT_USER']),
             'nickName': app.config['DEFAULT_USER']})


def getMe():
    me = mongo.db.users.find_one({'userName': app.config['DEFAULT_USER']})
    if me:
        return User(me)
    else:
        initMe()
        return getMe()
