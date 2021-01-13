
from app import app, fa
from flask import render_template, flash, redirect, url_for, request
from app.forms import LoginForm, RegistrationForm,  EditProfileForm, PostForm, DeletePost
from flask_login import current_user, login_user, logout_user, login_required
from app.models import User, db, Post
from werkzeug.urls import url_parse
import babel

@app.route('/')
@app.route('/index')
def index():
    posts = Post.query.all()
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
        current_user.username = form.username.data
        current_user.display_name = form.display_name.data
        db.session.commit()
        flash('Your changes has been saved!')
        return redirect(url_for('edit_profile'))
    elif  request.method == 'GET':
        form.username.data = current_user.username
        form.display_name.data = current_user.display_name
    return render_template('editprofile.html', title='Edit Profile', form=form)
    
@app.route('/posts', methods=['GET','POST'])
@login_required
def posts():
    form = PostForm()
    if form.validate_on_submit():
        p = Post(body=form.post.data, author=current_user)
        db.session.add(p)
        db.session.commit()
        return redirect(url_for('index'))
    return render_template('post.html', title='Post', form=form)

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
    db.session.delete(object)
    db.session.commit()
    return redirect(url_for('index'))