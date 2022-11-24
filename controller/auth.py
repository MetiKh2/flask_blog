from flask import Flask, render_template, request, redirect, url_for, flash, abort, __version__
from flask_login import login_user, current_user, logout_user
from validators.auth import LoginForm, RegisterForm, EditProfileForm, ChangePasswordForm
from models import User
from db_manager import db
from sqlalchemy import or_, and_
from werkzeug.security import generate_password_hash
from uuid import uuid4
from flask_mail import Message
from mail_manager import mail


class Auth:

    def __init__(self, *args, **kwargs):
        pass

    def Register(self):
        if current_user.is_authenticated:
            return redirect(url_for('main'))
        form = RegisterForm()
        if request.method == 'POST':
            if form.validate():
                username = request.form['username']
                email = request.form['email']
                password = request.form['password']
                user = db.session.query(User.Users).filter(
                    or_(User.Users.email == email, User.Users.username == username)).first()
                if not user:
                    newUser = User.Users(
                        username=username, email=email, password=generate_password_hash(password))
                    db.session.add(newUser)
                    result = db.session.commit()
                    if result != False:
                        flash('User Created Succesfully', 'success')
                    else:
                        flash('Error Server ,Please Try Again', 'danger')
                else:
                    flash('User Exist', 'warning')
                return redirect(url_for('Register'))
        return render_template('/auth/register.html', form=form)

    def Login(self):
        if current_user.is_authenticated:
            return redirect(url_for('main'))
        form = LoginForm()
        if request.method == 'POST':
            if form.validate():
                email = request.form.get('email')
                password = request.form['password']
                user = db.session.query(User.Users).filter(
                    User.Users.email == email).first()
                if not user:
                    flash('Email Or Password Are Wrong', 'danger')
                    return redirect(url_for('Login'))
                if user and user.IsOriginalPassword(password):
                    login_user(user, remember=True)
                    next_page = request.args.get('next')
                    return redirect(next_page) if next_page else redirect(url_for('main'))
                else:
                    flash('Email Or Password Are Wrong', 'danger')
                    return redirect(url_for('Login'))
        return render_template('/auth/login.html', form=form)

    def SignOut(self):
        logout_user()
        return redirect(url_for('Login'))

    def forget(self):
        if request.method == 'POST':
            if request.form['email'] != '':
                email = request.form['email']
                user = db.session.query(User.Users).filter(
                    User.Users.email == email).first_or_404()
                user.token = str(uuid4())
                db.session.add(user)
                db.session.commit()
                # Send Mail

                msg = Message(subject='Reset Password | Blog App',
                              sender='from@smtp.mailtrap.io', recipients=['to@smtp.mailtrap.io'])
                msg.body = 'This Email For Reset Your Password , Please Click to Link For Reset it !!'
                msg.html = f"""
                <a href="http://localhost:5000/resetpassword/{user.token}/{user.id}">Click To Reset Password</a>
            """

                mail.send(msg)
                flash('Email Be Sent', 'success')
                return redirect(url_for('forget'))
            return redirect(url_for('forget'))

        return render_template('/auth/forget.html')

    def reset_password(self , token , user_id):
        if request.method == 'POST':
            if request.form.get('password') == '' or len(request.form.get('password')) < 4:
                flash('Please Check Password Field , Its Wrong !' , 'danger')
                return redirect(url_for('reset_password' , token = token , user_id = user_id))
            user = User.Users.query.filter(and_(User.Users.id == user_id , User.Users.token == token)).first()
            user.password = generate_password_hash(request.form.get('password'))
            user.token = ''
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('SignOut'))
            
        return render_template('auth/reset.html' , token = token , user_id=user_id)