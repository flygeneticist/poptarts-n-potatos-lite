from flask import Flask, request, redirect, render_template, session ,jsonify
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required
from flask.ext.sqlalchemy import SQLAlchemy
from flask.ext.script import Shell, Manager


app = Flask(__name__)
manager = Manager(app)

# app config defaults and override from file
DEBUG = True
TESTING = True
SQLALCHEMY_DATABASE_URI = 'sqlite:////tmp/test.db'
app.config.from_object('config.DevelopmentConfig')

# setup database connection and create tables
db = SQLAlchemy(app)
db.create_all()

# hooks for routes


# routes
@app.route('/')
@app.route('/home')
def index():
    posts = Post.query.all()
    res = {}
    for post in posts:
        res[post.id] = {
            'title': post.title,
            'content': str(post.content)
        }
    return render_template('home.html', posts=jsonify(res));

@app.route('/blog/<post>')
def blog_post(post):
    res = Post.query.get_or_404(post)
    return render_template('blogPost.html', post=jsonify(res))

@app.route('/admin')
def admin_dash():
    user = str(request.headers.get('User'))
    if user != 'None':
        return 'Admin dashboard \n'+user
    else:
        return redirect('/admin/login')

@app.route('/admin/login', methods=['GET','POST'])
def login():
    session['user'] = None
    form = LoginForm()
    if form.validate_on_submit():
        session['user'] = form.email.data
        return redirect('/')
    else:
        return render_template('login.html', form=form)

# error handlers
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500

# Login Form logic using WTF
class LoginForm(Form):
    email = StringField('Email', validators=[Required()])
    password = PasswordField('Password', validators=[Required()])
    submit = SubmitField('Submit')

# Database Models
class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    posts = db.relationship('Post', backref='User')

    def __repr__(self):
        return '<Post %d>' % self.id

class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255))
    content = db.Column(db.Text())
    author = db.Column(db.Integer, db.ForeignKey('users.id'))
    comments = db.relationship('Comment', backref='Post')

    def __repr__(self):
        return '<Post %d>' % self.id

class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text())
    author = db.Column(db.String(255))
    parentId = db.Column(db.Integer, db.ForeignKey('posts.id'))

    def __repr__(self):
        return '<Comment %d>' % self.id

# Setup shell integration
def make_shell_context():
    return dict(app=app, db=db, User=User, Post=Post, Comment=Comment)
manager.add_command("shell", Shell(make_context=make_shell_context))


# run the app
if __name__ == '__main__':
    manager.run()
