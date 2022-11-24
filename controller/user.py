from flask import  current_app,Flask, render_template, request, redirect, url_for, flash, abort, __version__
from validators.auth import   ChangePasswordForm,EditProfileForm
from sqlalchemy import or_, and_
from models import User
from flask_login import   current_user, login_required
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from use import allowed_extension
import os
from db_manager import db
class Account:
    def __init__(self, *args, **kwargs):
        pass
    @login_required
    def Account(self):
        return render_template('/account/index.html')

    @login_required
    def AccountInfo(self):
     return render_template('/account/info.html')

    @login_required
    def ChangePassword(self):
        form = ChangePasswordForm()
        if request.method == 'POST':
         if form.validate():
            oldPassword = request.form['oldPassword']
            newPassword = request.form['newPassword']
            user = db.session.query(User.Users).filter(
                and_(User.Users.email == current_user.email, User.Users.username == current_user.username)).first()
            if user and user.IsOriginalPassword(oldPassword):
                user.password=generate_password_hash(newPassword)
                db.session.add(user)
                db.session.commit()
                print('hhh')
                flash('Password has been changed','success')
                return redirect(url_for('SignOut'))
            else :
                flash('Password is wrong','danger')
        return render_template('/account/changepassword.html', form=form)


    @login_required
    def AccountEdit(self):
        form = EditProfileForm()
        if request.method == 'POST':
            if form.validate():
                username = request.form['username']
                phone = request.form['phone']
                email = request.form['email']
                user =  db.session.query(User.Users).filter(
                    User.Users.email == current_user.email).first()
                other_user =  db.session.query(User.Users).filter(
                    or_(User.Users.email == email, User.Users.username == username)).first()
                if not other_user:
                    user.username = username
                    user.phone = phone
                    user.email = email
                    db.session.add(user)
                    db.session.commit()
                else:
                    flash('Email or username is already exist', 'danger')
                    return redirect(url_for('AccountEdit'))
                return redirect(url_for('AccountInfo'))
        return render_template('/account/edit.html', form=form)

    @login_required
    def AccountAvatar(self):
        if request.method == 'POST' and 'avatar' in request.files:
            avatar=request.files['avatar']
            filename=avatar.filename
            filesecure=secure_filename(filename)
            if not allowed_extension(filename):
                flash('Enter a valid image','danger')
                return redirect(url_for('AccountAvatar'))
            avatar.save(os.path.join(current_app.config['UPLOAD_DIR'],filesecure))
            user =  db.session.query(User.Users).filter(
                    and_(User.Users.email == current_user.email, User.Users.username == current_user.username)).first()
            if user :
                user.avatar=f'uploads/{filename}'
                db.session.add(user)
                db.session.commit()
                flash('Upload Succesfully','success')
                return redirect(url_for('AccountAvatar'))
        return render_template('/account/avatar.html')