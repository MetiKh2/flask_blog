from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Length, Email, EqualTo


class LoginForm(FlaskForm):
    email = StringField(name='email',
                        validators=[DataRequired('Email Field Is Required'), Email()])
    password = PasswordField(name='password',
                             validators=[DataRequired('Password Field Is Required'),
                                         Length(min=4, message='Higher Than 4')])

    submit = SubmitField()


class RegisterForm(FlaskForm):
    username = StringField(name='username',
                           validators=[DataRequired('Username Field Is Required')])
    email = StringField(name='email',
                        validators=[Email(), DataRequired('email Field Is Required')])
    password = PasswordField(name='password',
                             validators=[DataRequired('Password Field Is Required'),
                                         Length(min=4, message='Higher Than 4')])
    re_password = PasswordField(name='repassword',
                                validators=[DataRequired('Password Field Is Required'),
                                            Length(min=4, message='Higher Than 4'), EqualTo('password', 'Password and re password are wrong')])

    submit = SubmitField()


class EditProfileForm(FlaskForm):
    username = StringField(name='username',
                           validators=[DataRequired('Username Field Is Required')])
    phone = StringField(name='phone',
                        validators=[DataRequired()])
    email = StringField(name='email',
                        validators=[DataRequired('Email Field Is Required'), Email()])
    submit = SubmitField('Update Profile')


class ChangePasswordForm(FlaskForm):
    oldPassword = PasswordField(name='oldPassword',
                                validators=[DataRequired(),
                                            Length(min=4)])


    newPassword = PasswordField(name='newPassword',
                            validators=[DataRequired(),
                                        Length(min=4)])
    rePassword = PasswordField(name='rePassword',
                            validators=[DataRequired(),
                                        Length(min=4), EqualTo('newPassword', 'Password and re password are wrong')])

    submit = SubmitField('Update Profile')
