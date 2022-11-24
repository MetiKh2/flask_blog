from flask import Flask, render_template, request, redirect, url_for, flash, abort, __version__
from flask_login import current_user, login_required
from db_manager import db
from sqlalchemy import or_
from models import User,Article
from werkzeug.security import generate_password_hash
from validators.admin import CreateUserForm, EditUserForm


class Admin:

    def __init__(self, *args, **kwargs):
        pass

    @login_required
    def Index(self):
        if not current_user.admin:
            return redirect(url_for('Account'))

        return render_template('/admin/index.html')

    @login_required
    def get_all_users(self):
        if not current_user.admin:
            return redirect(url_for('Account'))
        if request.method == 'POST':
            db.session.query(User.Users).filter(
                User.Users.id == int(request.args.get('id'))).delete()
            db.session.commit()
        users = db.session.query(User.Users).all()
        return render_template('/admin/user/list.html', users=users)

    def add_user(self):
        if not current_user.admin:
            return redirect(url_for('Account'))
        form = CreateUserForm()
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
        return render_template('/admin/user/create.html', form=form)

    def edit_user(self):
        if not current_user.admin:
            return redirect(url_for('Account'))
        form = EditUserForm()
        user = db.session.query(User.Users).filter(
            User.Users.id == int(request.args.get('id'))).one()
        if not user:
            abort(404)
        if request.method == 'POST':
            if form.validate():
                username = request.form['username']
                phone = request.form['phone']
                email = request.form['email']
                other_user = db.session.query(User.Users).filter(
                    or_(User.Users.email == email, User.Users.username == username)).first()
                print(other_user)
                if not other_user or other_user.id == user.id:
                    user.username = username
                    user.phone = phone
                    user.email = email
                    db.session.add(user)
                    db.session.commit()
                else:
                    flash('Email or username is already exist', 'danger')
                    return redirect(url_for('edit_user'))
                return redirect(url_for('get_all_users'))
        return render_template('/admin/user/edit.html', form=form, user=user)

    def approve_comment (self,comment_id):
        comment=db.session.query(Article.Comments).filter(Article.Comments.id==comment_id).first()
        comment.status=True
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('get_all_comments'))
    
    def delete_comment (self,comment_id):
        db.session.query(Article.Comments).filter(Article.Comments.id==comment_id).delete()
        db.session.commit()
        return redirect(url_for('get_all_comments'))


    def get_all_comments (self):
        comments=db.session.query(Article.Comments).all()
        return render_template('/admin/comments.html',comments=comments)
        