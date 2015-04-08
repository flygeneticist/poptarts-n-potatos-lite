from flask import Flask, request, redirect, render_template
from flask.ext.wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import Required

app = Flask(__name__)

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

@app.route('/admin/login')
def login():
    return 'Login page for admin dashboard'


# run the app
if __name__ == '__main__':
    app.run(debug=True)

