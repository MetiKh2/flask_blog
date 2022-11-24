from flask import Flask, render_template, request, redirect, url_for, flash, abort, __version__
from models.Article import Articles,Comments
from db_manager import db
from flask_login import current_user

class Home:

    def __init__(self, *args, **kwargs):
        pass

    def main(self):
        page = request.args.get('page', default=1, type=int)
        articles = Articles.query.paginate(page=page, per_page=2)
        return render_template('home.html', articles=articles)

    def single(self, id):
        article = db.session.query(Articles).filter(Articles.id == id).first()
        if request.method == 'POST':
            text=request.form['text']
            new_comment=Comments(text=text,article_id=id,user_id=current_user.id)
            db.session.add(new_comment)
            db.session.commit()
        else:
            article.views = article.views+1
            db.session.add(article)
            db.session.commit()
        comments=db.session.query(Comments).filter(Comments.article_id==id).all()
        return render_template('single.html', article=article,comments=comments)
