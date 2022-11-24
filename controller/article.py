from flask import current_app, render_template, request, redirect, url_for, flash, abort, __version__
from db_manager import db
from werkzeug.utils import secure_filename
from validators.article import CreatePostForm,EditPostForm
from use import allowed_extension
import os
from models.Article import Articles,Category
from flask_login import current_user
from sqlalchemy import and_


class Article:
    def __init__(self, *args, **kwargs):
        pass

    def index_post(self):
        return render_template('home.html')

    def create_post(self):
        form = CreatePostForm()
        if request.method == 'POST':
            category = request.form['category']
            print(category)
            if form.validate_on_submit() and category:
                subject = request.form['subject']
                content = request.form['content']
                publish = 0
                if  request.form['publish']=='on':
                    publish=1
                thumb = request.files['thumb'] if 'thumb' in request.files else None
                if thumb is not None:
                    filename = thumb.filename
                    filesecure = secure_filename(filename)
                    if not allowed_extension(filename):
                        flash('Enter a valid image', 'danger')
                    else:
                        thumb.save(os.path.join(
                        current_app.config['UPLOAD_DIR'], filesecure))
                new_post = Articles(subject=subject, content=content, publish=publish,
                                    writer=current_user.id, thumb=f'uploads/{thumb.filename}',category_id=int(category))
                db.session.add(new_post)
                db.session.commit()
                flash('Article saved successfully', 'success')
                return redirect(url_for('create_post'))
        categories=db.session.query(Category).all()
        return render_template('/admin/post/create.html', form=form,categories=categories)

    def get_all_articles(self):
        if request.method == 'POST':
             db.session.query(Articles).filter(
                Articles.id == int(request.args.get('id'))).delete()
             db.session.commit()
        getAll = Articles.query.all()
        return render_template('/admin/post/list.html', articles=getAll)
    
    def edit_post(self):
        if not current_user.admin:
            return redirect(url_for('Account'))
        form = EditPostForm()
        article = db.session.query(Articles).filter(
            Articles.id == int(request.args.get('id'))).first()
        if not article:
            abort(404)
        if request.method == 'POST':
            category = request.form['category']
            if form.validate() and category:
                subject = request.form['subject']
                content = request.form['content']
                publish = True if request.form['publish'] == 'on'else False
                thumb = request.files['thumb'] if 'thumb' in request.files else None
                if thumb is not None:
                    filename = thumb.filename
                    filesecure = secure_filename(filename)
                    if not allowed_extension(filename):
                        flash('Enter a valid image', 'danger')
                    else:
                        thumb.save(os.path.join(
                        current_app.config['UPLOAD_DIR'], filesecure))
                article.subject=subject
                article.content=content
                article.publish=publish
                article.category_id=category
                article.thumb=f'uploads/{thumb.filename}'
                db.session.add(article)
                db.session.commit()
                return redirect(url_for('get_all_articles'))
        categories=db.session.query(Category).all()
        return render_template('/admin/post/edit.html', form=form, categories=categories,article=article)


    def create_category(self):
        if request.method == 'POST':
            if request.form['name']!='':
                name = request.form['name']
                new_category = Category(name=name)
                db.session.add(new_category)
                db.session.commit()
                flash('Category saved successfully', 'success')
                return redirect(url_for('create_category'))
        return render_template('/admin/category/create.html')

    def get_all_categories(self):
        if request.method == 'POST':
             db.session.query(Category).filter(
                Category.id == int(request.args.get('id'))).delete()
             db.session.commit()
        getAll = Category.query.all()
        return render_template('/admin/category/index.html', categories=getAll)
    
    def edit_category(self):
        if not current_user.admin:
            return redirect(url_for('Account'))
        category = db.session.query(Category).filter(
            Category.id == int(request.args.get('id'))).first()
        if not category:
            abort(404)
        if request.method == 'POST':
            if request.form['name']:
                name = request.form['name']
                category.name=name
                db.session.add(category)
                db.session.commit()
                return redirect(url_for('get_all_categories'))
        return render_template('/admin/category/edit.html',  category=category)

    def view_category(self,name):
        category=db.session.query(Category).filter(Category.name==name).first()
        articles=db.session.query(Articles).filter(and_(Articles.category_id==category.id,Articles.publish==True))
        return render_template('categories.html',  articles=articles)
        
    def search(self):
        print('a')
        query=request.args.get('s')
        articles=db.session.query(Articles).filter(Articles.subject.contains(query)).all()
        return render_template('search.html',  posts=articles,search_input=query)
        