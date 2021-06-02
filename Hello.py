from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)


class BLogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default="N/A")
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)

    def __repr__(self):
        return 'Blog post' + str(self.id)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

    def __repr__(self):
        return 'Users' + str(self.id)


all_posts = [
    {
        'title': 'Post 1',
        'content': ' This is the content for post',
        'author': 'kishore'

    },
    {
        'title': 'Post 2',
        'content': ' This is the content for post'
    },
    {
        'title': 'Post 3',
        'content': ' This is the content for post'
    },
]

users = [
    {
        'email': 'kishore19.bandi@gmail.com',
        'password': 'kish123'

    },
    {
        'email': 'kishore19.reddy@gmail.com',
        'password': 'kish234'

    }
]


@app.route("/")
def index():
    return render_template('index.html')


@app.route("/home")
def home():
    all_posts = BLogPost.query.order_by(BLogPost.date_posted)

    return render_template('home.html',  posts=all_posts)


@app.route("/login")
def login():

    return render_template('login.html')


@app.route("/signup")
def signup():

    return render_template('signup.html')


@app.route("/logincheck", methods=['GET', 'POST'])
def logincheck():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        users = User.query.order_by(User.email).all()
        for user in users:
            print(user.email)
            print(user.password)

            if(user.email == email and user.password == password):

                return render_template('posts.html')
    else:
        return render_template('login.html')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        confirmpassword = request.form['confirm-password']
        if(password == confirmpassword):
            new_user = User(
                email=email,  password=password)
            db.session.add(new_user)
            db.session.commit()
            return redirect('/posts')

            return render_template('login.html')

    else:
        return render_template('login.html')


@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BLogPost(
            title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BLogPost.query.order_by(BLogPost.date_posted)

        return render_template('posts.html', posts=all_posts)


@app.route("/<string:name>")
def hello(name):
    return " Hello world "+name


@app.route('/onlyget')
def get_only():
    return "you can get only"


@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BLogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')


@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = BLogPost.query.get_or_404(id)
    if request.method == 'POST':

        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']

        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)


@app.route('/posts/new', methods=['GET', 'POST'])
def new_post():
    if request.method == 'POST':

        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        new_post = BLogPost(
            title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')


if __name__ == '__main__':
    db.create_all()

    app.run(debug=True)
