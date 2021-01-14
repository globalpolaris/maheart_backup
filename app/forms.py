from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import DataRequired, ValidationError, Email, EqualTo, Length, Optional, Regexp
from app.models import User
from wtforms.widgets.core import Select, html_params

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[Length(min=1,max=32), DataRequired()], render_kw={'placeholder':'username'})
    password = PasswordField('Password', validators=[DataRequired()], render_kw={'placeholder':'password'})
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegistrationForm(FlaskForm):
    username = StringField('Username',validators=[Length(min=1,max=32), Regexp(r'^[\w.]+$'), DataRequired()], render_kw={'placeholder':'username'})
    display_name = StringField('Display name', validators=[Length(min=1,max=32), DataRequired()], render_kw={'placeholder':'name on post'})
    email = StringField('Email', validators=[Length(min=1,max=64), DataRequired(), Email()], render_kw={'placeholder':'email@email.com'})
    password = PasswordField('Password', validators=[Length(min=8,max=32), DataRequired()], render_kw={'placeholder':'********'})
    password2 = PasswordField(
        'Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exists')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user is not None:
            raise ValidationError('Email already taken')

class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[Length(max=32), Regexp(r'^[\w.]+$'), Optional()], render_kw={'placeholder':'New username'})
    display_name = StringField('Display name', validators=[Length(max=32)])
    submit = SubmitField('Save')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user is not None:
            raise ValidationError('Username already exists')

class PostForm(FlaskForm):
    post = StringField('Post', validators=[Length(min=1,max=255),DataRequired()], render_kw={'placeholder':'Ceritakan ceritamu...'})
    submit = SubmitField('Send')

class DeletePost(FlaskForm):
    delete = SubmitField('Delete')
