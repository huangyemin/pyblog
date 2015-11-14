from flask import Flask,render_template,request,session,redirect,url_for
import datetime
from flask.ext.pymongo import PyMongo

app = Flask(__name__)
mongo = PyMongo(app)

@app.route('/')
def index():
    if app.debug:
        blogs = [{'id':'1','title': '创新', 'postTime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'author': '星奕',
              'summary': '创新创新创新创新创新创新创新'},
             {'id':'2','title': '教育', 'postTime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'author': '星奕',
              'summary': '教育教育教育教育教育教育教育教育'},
             {'id':'3','title': '科技', 'postTime': datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'author': '星奕',
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
        blog = mongo.db.blogs.find_one_or_404({'_id':id})
    return render_template('blog.html', blog=blog)

@app.route('/postBlog',methods=['GET','POST'])
def postBlog():
    if not 'user' in session:
        return redirect(url_for('toLogin'))
    blog = request.json
    mongo.db.blogs.insert(blog)

@app.route('/toLogin')
def toLogin():
    return render_template('login.html')

@app.route('/about')
def about():
    return render_template('about.html')


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)
