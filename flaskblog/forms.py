from flask_wtf import FlaskForm
from flask_login import current_user
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField,PasswordField,SubmitField,BooleanField, TextAreaField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from flaskblog.models import User
from flask_ckeditor import CKEditorField

class RegistrationForm(FlaskForm):
    username = StringField('Username (Max 25 Character)', validators= [DataRequired(), Length(min=2, max=25)])
    email = StringField('Email', validators= [DataRequired(), Email()])
    password = PasswordField('Password', validators= [DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')
    
    def validate_username(self, username):
        user = User().query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("That username is already taken")

    def validate_email(self, email):
        user = User().query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("That email is already used")

class LoginForm(FlaskForm):
    email = StringField('Email', validators= [DataRequired(), Email()])
    password = PasswordField('Password', validators= [DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Login')


class UpdateAccountForm(FlaskForm):
    username = StringField('Username (Max 25 Character)', validators= [DataRequired(), Length(min=2, max=25)])
    email = StringField('Email', validators= [DataRequired(), Email()])
    picture = FileField('Update profile picture', validators = [FileAllowed(["jpg", "png", "jpeg"])])
    submit = SubmitField('Submit')
    role = StringField('Role')
    
    def validate_username(self, username):
        if username.data != current_user.username:
            user = User().query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("That username is already taken")

    def validate_email(self, email):
        if email.data != current_user.email:
            user = User().query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("That email is already used")
            

class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = CKEditorField('Content', validators=[DataRequired()])
    thumbnail = FileField('Thumbnail', validators = [FileAllowed(["jpg", "png", "jpeg"])])
    submit = SubmitField('Post')