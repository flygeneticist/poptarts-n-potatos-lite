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

# run the app
if __name__ == '__main__':
    manager.run()
