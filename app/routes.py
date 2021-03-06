
from app import app, fa
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm,  EditProfileForm, PostForm, DeletePost, CommentForm
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, db, Post, Comment
from werkzeug.urls import url_parse
import babel

@app.route('/')
@app.route('/index')
def index():
    posts = Post.query.order_by(Post.timestamp.desc())
    return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_displayname(form.display_name.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        # flash('You can now login with your username.')
        return redirect(url_for('login'))
    return render_template('signup.html', title='Sign Up', form=form)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm()
    if form.validate_on_submit():
        if form.username.data is not None:
            current_user.username = form.username.data
        current_user.display_name = form.display_name.data
        db.session.commit()
        flash('Your changes has been saved!')
        return redirect(url_for('edit_profile'))
    elif  request.method == 'GET':
        # form.username.data = current_user.username
        form.display_name.data = current_user.display_name
    return render_template('editprofile.html', title='Edit Profile', form=form)
    
@login_required
@app.route('/write', methods=['POST'])
def write():
    pos = request.form.get('post1')
    db.session.add(Post(body=pos, author=current_user))
    db.session.commit()
    return redirect(url_for('index'))

@app.route('/post/<int:id>', methods=['GET','POST'])
def post(id):
    post = Post.query.get_or_404(id)
    
    return render_template('post.html', title='Post', post=post, id=id)

@login_required
@app.route('/post/<int:id>/comment', methods=['POST'])
def comment(id):
    comment = request.form.get('cmnt')
    post = Post.query.get_or_404(id)
    db.session.add(Comment(body=comment, author=current_user, post=post))
    db.session.commit()
    return redirect(url_for('post', id=id))

    

@app.template_filter()
def format_datetime(value, format='medium'):
    if format == 'full':
        format="EEEE, d-MM-y"
    elif format == 'medium':
        format="HH:mm"
    return babel.dates.format_datetime(value, format)

@login_required
@app.route('/delete/<int:id>', methods=['POST'])
def remove(id):
    object = Post.query.get_or_404(id)
    if object.author != current_user:
        abort(403)
    db.session.delete(object)
    db.session.commit()
    return redirect(url_for('index'))