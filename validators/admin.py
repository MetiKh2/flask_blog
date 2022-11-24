from flask_wtf import FlaskForm 
from wtforms.fields import StringField , PasswordField , SubmitField
from wtforms.validators import DataRequired , Length , Email , EqualTo

class CreateUserForm(FlaskForm):
    username = StringField(name='username' , 
    validators=[DataRequired('Name Field is Required')])

    email = StringField(name='email' , 
    validators=[DataRequired('Email Field Is Required') , Email('Email is InValid')])

    password = PasswordField(name='password' , 
    validators=[DataRequired('Password Field Is Required !') , 
    Length(min=4 , message='Password Is Less Than 4 Character')])

    confirm = PasswordField(name='confirm' , 
    validators=[DataRequired('Confirm Password Field Is Required !') , 
    Length(min=4 , message='Password Is Less Than 4 Character')
    ,EqualTo('password' , 'Confirm Does Not Match With Password')])

    submit = SubmitField('Create User')

class EditUserForm(FlaskForm):
    username = StringField(name='username' , 
    validators=[DataRequired('Name Field is Required')])

    email = StringField(name='email' , 
    validators=[DataRequired('Email Field Is Required') , Email('Email is InValid')])
    
    phone = StringField(name='phone',
                        validators=[DataRequired()])

    submit = SubmitField('Edit User')