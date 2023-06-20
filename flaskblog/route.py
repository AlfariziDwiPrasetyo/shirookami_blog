import os
import secrets
from PIL import Image
from flask import render_template, flash, redirect,url_for, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

@app.route("/")
@app.route("/home")
def home():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.date.desc()).paginate(page=page, per_page=3)
    return render_template('home.html', posts=posts, title='Posts')

@app.route("/about")
def about():
    return render_template('about.html', title='About')

@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('logout'))

    form = RegistrationForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(user)
        db.session.commit()
        flash(f'Your account has been created')
        return redirect(url_for('home'))
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():

    if current_user.is_authenticated:
        return redirect(url_for('logout'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            flash(f"Welcome {current_user.username}")
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash('Wrong email or password', 'gray-900')
    return render_template('login.html', title='Login', form=form)




@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))



@app.route("/account")
@login_required
def account():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    title_user = 'User'
    return render_template('account.html', title='Account', image_file = image_file, title_user=title_user)



def save_picture_profile(form_picture):
    random_hex = secrets.token_hex(8)
    _, _ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + _ext
    picture_path = os.path.join(app.root_path, 'img/profile_pics', picture_fn)

    size = (192, 192)
    i = Image.open(form_picture)
    i.thumbnail(size)

    i.save(picture_path)
    return picture_fn 


@app.route("/edit", methods=['GET', 'POST'])
@login_required
def edit():
    form = UpdateAccountForm()
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture_profile(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.role = form.role.data
        db.session.commit()
        return redirect(url_for('account'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.role.data = current_user.role
    return render_template('edit.html', title='Edit', form=form)



def save_picture_tn(form_picture):
    random_hex = secrets.token_hex(8)
    _, _ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + _ext
    picture_path = os.path.join(app.root_path, 'img/profile_pics', picture_fn)

    size = (1080, 1920)
    i = Image.open(form_picture)
    i.thumbnail(size)

    i.save(picture_path)
    return picture_fn 

@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        picture_file = save_picture_tn(form.thumbnail.data)
        post = Post(title=form.title.data, content=form.content.data, author=current_user, thumbnail=picture_file)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created')
        return redirect(url_for('home'))
    return render_template('create_post.html', title="New Post", form=form, legend='What is in your mind ?')

@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.thumbnail = form.thumbnail.data
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', form=form, legend='Update Post')

@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted')
    return redirect(url_for('home'))
