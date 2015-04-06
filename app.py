from flask import Flask, request, redirect, render_template

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

