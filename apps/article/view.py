from flask import Blueprint, render_template, request, redirect, url_for, session, g, jsonify
from apps.article.models import Article,Comment,Article_type
from apps.user.model import User
from exts import db

article_bp = Blueprint('article', __name__, url_prefix='/article')


@article_bp.route('/all', endpoint='all')
def all_article():
    user = User.query.filter(User.isdelete == False).all()
    types = Article_type.query.all()
    arts = Article.query.all()
    return render_template('article/article.html', types = types,arts=arts, user=user)


@article_bp.route('/publish', endpoint='publish', methods=['GET', 'POST'])
def publish_article():
    if request.method == 'POST':
        title = request.form.get('title')
        content = request.form.get('content')
        type_id = request.form.get('type')

        art = Article()
        art.title = title
        art.content = content
        art.type_id = type_id
        art.user_id = g.user.id

        db.session.add(art)
        db.session.commit()

        return redirect(url_for('user.index'))

    return render_template('article/add.html')

@article_bp.route('/comment', endpoint='comment')
def comment_article():
    aid = request.args.get('aid')
    art = Article.query.get(aid)
    # types = Article_type.query.all()
    content = request.args.get('content')
    comment = Comment()
    comment.article_id = aid
    comment.user_id = g.user.id
    comment.comment = content
    db.session.add(comment)
    db.session.commit()

    return render_template('article/detail.html', art=art,user=g.user, types =g.types)


@article_bp.route('/type',endpoint='type')
def type_article():
    uid = session.get('uid')
    user = None
    if uid:
        user = User.query.get(uid)

    tid = request.args.get('type')
    page = request.args.get('page',1)
    page = int(page)
    articles = Article.query.filter(Article.type_id == tid).order_by(-Article.pdateTime).paginate(page=page,per_page=4)

    return  render_template('article/types.html',user= user,types=g.types,tid = tid, articles = articles)

@article_bp.route('/detail', endpoint='detail')
def detail_article():
    aid = request.args.get('aid')
    art = Article.query.get(aid)
    uid = session.get('uid',None)
    if uid:
        user = User.query.get(uid)
    else:
        user = None
    return render_template('article/detail.html', art=art, user=user,types=g.types)


@article_bp.route('/love', endpoint='love')
def love_article():
    aid = request.args.get('aid')
    art = Article.query.get(aid)
    no = request.args.get('no')
    if not no:
        art.love_num -= 1
        print(art.love_num)
        db.session.commit()
        return jsonify(num=art.love_num)
    else:
        art.love_num += 1
        print(art.love_num, "------")
        db.session.commit()
        return jsonify(num=art.love_num)

    return render_template('article/detail.html', art=art)


@article_bp.route('/save',endpoint='save')
def save_article():
    aid = request.args.get('aid')
    art = Article.query.get(aid)
    no = request.args.get('no')

    if not no:
        art.save_num -= 1
        db.session.commit()
        return jsonify(num=art.save_num)
    else:
        art.save_num += 1
        db.session.commit()
        return jsonify(num=art.save_num)

