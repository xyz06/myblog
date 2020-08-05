from exts import db
from datetime import datetime

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(16), nullable=False, unique= True)
    pwd = db.Column(db.String(64), nullable= False)
    phone = db.Column(db.String(11), unique =True)
    isdelete = db.Column(db.Boolean, default= False)
    rdatetime = db.Column(db.DateTime, default=datetime.now)
    icon = db.Column(db.String(100))
    articles = db.relationship('Article', backref='user')
    comments = db.relationship('Comment', backref='user')
    messages = db.relationship('Messageboard', backref='user')
    def __str__(self):
        return self.username

class Photo(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    photo_name = db.Column(db.String(50), nullable=False)
    photo_datetime = db.Column(db.DateTime, default=datetime.now)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __str__(self):
        return self.photo_name


class Messageboard(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.String(255), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    mdatetime = db.Column(db.DateTime, default=datetime.now)


class Aboutme(db.Model):
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    content = db.Column(db.BLOB, nullable=False)
    create_datetime = db.Column(db.DateTime, default=datetime.now)
    update_datetime = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'),nullable=False, unique=True)

    user = db.relationship('User', backref='aboutme')
