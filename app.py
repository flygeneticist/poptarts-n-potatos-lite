from flask import Flask, request, redirect

app = Flask(__name__)

# hooks for routes


# routes
@app.route('/')
def home():
    return 'I\'m a home page';

@app.route('/blog/<post>')
def blog_post(post):
    return 'Blog post: %s' % post

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

