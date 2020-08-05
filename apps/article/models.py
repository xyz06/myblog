from exts import db
from datetime import datetime

class Article_type(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    art_type = db.Column(db.String(20), nullable=False)
    articles = db.relationship('Article', backref='type')

class Article(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(60), nullable=False)
    content = db.Column(db.Text, nullable=False)
    pdateTime = db.Column(db.DateTime,default=datetime.now)
    click_num = db.Column(db.Integer, default=0)
    love_num = db.Column(db.Integer, default=0)
    save_num = db.Column(db.Integer, default=0)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    type_id = db.Column(db.Integer, db.ForeignKey('article_type.id'), nullable=False)

    comments = db.relationship('Comment', backref='article')


class Comment(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    comment = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    article_id = db.Column(db.Integer, db.ForeignKey('article.id'), nullable=False)
    cdatetime = db.Column(db.DateTime, default=datetime.now)

#
# class User_comment(db.Model):
#     id = db.Column(db.Integer, primary_key=True, autoincrement=True)
#     user_comment_user = db.Column(db.String(255), nullable=False)
#     from_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
#     to_id = db.Column()
#
#     comment_id = db.Column(db.Integer, db.ForeignKey('comment.id'), nullable=False)
#
