from flask import Flask, request, redirect, render_template, session
from flask.ext.wtf import Form
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)

# app config defaults and override from file
DEBUG = True
TESTING = True
app.config.from_object('config.DevelopmentConfig')

# hooks for routes


# routes
@app.route('/')
def home():
    posts = [   {'title': 'Post #1', 'url': 'post-1', 'summary':'This is a cool post about...'},
                {'title': 'Post #2', 'url': 'post-1', 'summary':'This is a cool post about somthing else...'}
            ]
    return render_template('home.html', posts=posts);

@app.route('/blog/<post>')
def blog_post(post):
    post = {'title': 'Post #1', 'url': 'post-1', 'summary':'This is a cool post about...', 'content': '<p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam,quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo onsequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p><p>Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.</p>'}
    return render_template('blogPost.html', post=post)

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
    app.run(debug=DEBUG)
