from flask import Blueprint, render_template, request, url_for, redirect, jsonify, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from apps.user.model import User, Photo, Aboutme,Messageboard
from apps.article.models import Article, Article_type
from sqlalchemy import or_, and_, not_
from datetime import datetime
from exts import db
from hashlib import sha3_256
import os
import random
from settings import Config
from apps.user.sendmsg import SmsSendAPIDemo
from apps.utils.util_qiniu import upload_qn, delete_qn

user_bp = Blueprint('user', __name__, url_prefix='/user/')

required_login_list = ['/user/center',
                       '/user/update',
                       '/article/publish',
                       '/article/comment',
                       '/user/photo',
                       '/user/photo_del',
                       '/user/about_me',
                       '/user/showme']
ALLOWED_EXTENSIONS = ['jpg', 'png']


@user_bp.before_app_request
def before_req():
    if request.path in required_login_list:
        id = session.get('uid')
        if not id:
            g.types = Article_type.query.all()
            return render_template('user/login.html')
        else:
            g.user = User.query.get(id)
            g.types = Article_type.query.all()

    g.types = Article_type.query.all()


# 自定义模板过滤器
@user_bp.app_template_filter('cdecode')
def content_decode(content):
    # content =content.decode('utf-8')
    return content[:10]


@user_bp.app_template_filter('cdecode1')
def content_decode(content):
    content = content.decode('utf-8')
    return content


@user_bp.route('/')
def index():
    # 会话机制
    # 1.cookie获取
    # uid = request.cookies.get('uid', None)

    # 2.session获取
    uid = session.get('uid', None)
    page = int(request.args.get('page', '1'))
    # print(page)
    paginate = Article.query.order_by(-Article.pdateTime).paginate(page=page, per_page=3)
    # print(paginate.items, paginate.page, paginate.has_next, paginate.has_prev, paginate.total, paginate.total)
    types = Article_type.query.all()
    if uid:
        user = User.query.get(uid)
        return render_template('user/index.html', user=user, paginate=paginate, types=types)
    return render_template('user/index.html', paginate=paginate, types=types)


@user_bp.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form.get('username')
        pwd = request.form.get('pwd')
        repwd = request.form.get('cpwd')
        phone = request.form.get('phone')
        select_user = User.query.filter(User.username == username).all()
        if len(select_user) == 0:
            if pwd == repwd:
                user = User()
                user.username = username
                user.pwd = generate_password_hash(pwd)
                user.phone = phone

                db.session.add(user)
                db.session.commit()
                return redirect(url_for('user.login'))
            else:
                return '密码不一致'
        return render_template('user/register.html', msg='用户名已存在')

    return render_template('user/register.html')


@user_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        f = request.args.get('f')
        if f == '1':
            username = request.form.get('username')
            password = request.form.get('pwd')
            # new_password = generate_password_hash(password)
            # new_password = sha3_256(password.encode('utf-8')).hexdigest()

            user = User.query.filter(User.username == username).first()

            flag = check_password_hash(user.pwd, password)
            if flag:
                # 会话机制
                # 1.cookie
                # response = redirect(url_for('user.index'))
                # response.set_cookie('uid', str(user.id), max_age=1800)
                # return response
                # 2session
                session['uid'] = user.id
                return redirect(url_for('user.index'))
            else:
                return render_template('user/login.html', msg='用户名或密码错误')
        elif f == '2':
            phone = request.form.get('phone')
            yzm = request.form.get('yzm')
            code = session.get(phone)
            print(code, yzm)
            if code == yzm:
                user = User.query.filter(User.phone == phone).first()
                if user:
                    session['uid'] = user.id
                    return redirect(url_for('user.index'))
                else:
                    render_template('user/login.html', msg='手机为注册')
            else:
                render_template('user/login.html', msg='验证码有误')

    return render_template('user/login.html')


@user_bp.route('/logout')
def logout():
    # 会话机制
    # 1.cookie删除
    # response = redirect(url_for('user.index'))
    # response.delete_cookie('uid')
    # return response

    # 2.session删除
    #  (1)del session['uid']
    #  (2)
    session.clear()
    return redirect(url_for('user.index'))


@user_bp.route('/sendmsg')
def sendmsg():
    phone = request.args.get('phone')
    user = User.query.filter(User.phone == phone).first()
    if user:
        SECRET_ID = "9407e698533cf693d5ed09bbaca9f10a"  # 产品密钥ID，产品标识
        SECRET_KEY = "653853c9393465ca036021bcafb1ca60"  # 产品私有密钥，服务端生成签名信息使用，请严格保管，避免泄露
        BUSINESS_ID = "556ac3e71eeb435db2cd1b1f723b8b1d"  # 业务ID，易盾根据产品业务特点分配
        api = SmsSendAPIDemo(SECRET_ID, SECRET_KEY, BUSINESS_ID)

        params = {
            "mobile": phone,
            "templateId": "1",
            "paramType": "json",
            "params": "json格式字符串"
            # 国际短信对应的国际编码(非国际短信接入请注释掉该行代码)
            # "internationalCode": "对应的国家编码"
        }
        ret = api.send(params)
        # if ret is not None:
        #     if ret["code"] == 200:
        #         taskId = ret["data"]["taskId"]
        #         print("taskId = %s" % taskId)
        #         return jsonify(code=200, msg='发送成功')
        #     else:
        #         print("ERROR: ret.code=%s,msg=%s" % (ret['code'], ret['msg']))
        #         return jsonify(code=400, msg='手机号码未注册')
        session[phone] = '1234'
        return jsonify(code=200, msg='发送成功')


    else:
        # return redirect(url_for('user.loign'))
        return jsonify(code=400, msg='手机号码未注册')


@user_bp.route('/center', endpoint='center', methods=['GET', 'POST'])
def user_center():
    types = Article_type.query.all()
    photos = Photo.query.filter(Photo.user_id == g.user.id).all()
    board = Messageboard.query.order_by(-Messageboard.mdatetime).all()

    return render_template('user/center.html', user=g.user, types=types, photos=photos, board=board)


@user_bp.route('/search')
def search():
    key = request.args.get('search')
    user_list = User.query.filter(or_(User.username.contains(key), User.phone.contains(key))).all()
    return render_template('user/center.html', users=user_list)


@user_bp.route('/delete', endpoint='delete')
def user_delete():
    id = request.args.get('id')
    user = User.query.get(id)
    user.isdelete = True
    db.session.commit()

    return redirect(url_for('user.center'))


@user_bp.route('/update', endpoint='update', methods=['GET', 'POST'])
def user_update():
    if request.method == 'POST':
        username = request.form.get('username')
        phone = request.form.get('phone')
        icon = request.files.get('icon')
        print('>>>>>>>',icon)
        # users = User.query.filter(or_(User.phone == phone, User.username == username)).all()
        # print(len(users))
        icon_name = icon.filename
        suffix = icon_name.rsplit('.')[-1]
        if suffix in ALLOWED_EXTENSIONS:
            icon_name = secure_filename(icon_name)
            file_path = os.path.join(Config.UPLOAD_ICON_PATH, icon_name)
            icon.save(file_path)

            user = g.user
            user.username = username
            user.phone = phone
            path = 'upload/icon/'
            user.icon = os.path.join(path, icon_name)
            print(user.icon, icon_name)
            db.session.commit()
            return redirect(url_for('user.center'))

        else:
            return render_template('user/center.html', user=g.user, msg='用户名或手机已存在')
            # return render_template('user/update.html', user=g.user, msg='用户名已存在')

    return render_template('user/center.html')


@user_bp.route('/photo', endpoint='photo', methods=['GET', 'POST'])
def photo_upload():
    photo = request.files.get('photo')

    # 云存储
    # ret, info = upload_qn(photo)
    # if info['status_code'] == 200:
    #     ph = Photo()
    #     ph.photo_name = ret['key']
    #     ph.user_id = g.user.id
    #     db.session.add(ph)
    #     db.session.commit()
    #     return '上传成功'
    # else:
    #     return '上传失败'

    # 本地存储
    if photo:
        filename = photo.filename
        ext = filename.rsplit('.')[1]
        if ext in ALLOWED_EXTENSIONS:
            new_filename = filename.rsplit('.')[0] + '_' + str(random.randint(1, 1000)) + '.' + ext
            print(new_filename)
            ph = Photo()
            ph.photo_name = new_filename
            ph.user_id = g.user.id
            db.session.add(ph)
            db.session.commit()

            photo.save(os.path.join(Config.UPLOAD_IMAGES_PATH, new_filename))
            return '上传成功'

        else:
            return '文件格式错误'
    return '没有文件'


@user_bp.route('/photo_del')
def photo_del():
    pid = request.args.get('pid')
    photo = Photo.query.get(pid)
    # filename = photo.photo_name
    # info = delete_qn(filename)
    # if info.status_code == 200:
    #     #先删除云后删除数据库
    #     db.session.delete(photo)
    #     db.session.commit()
    #     return redirect(url_for('user.center'))
    # else:
    #     return '删除失败',400

    # 本地删除
    if photo:
        db.session.delete(photo)
        db.session.commit()
        return redirect(url_for('user.center'))
    else:
        return render_template('error.html', msg='删除失败', referer=request.headers.get('Referer'))


@user_bp.route('/select')
def user_select():
    # User.query.get(1)   #select *from User where id =1
    # User.query.filter(User.username).all()  #常用
    # User.query.filter_by(username='xyz').first()
    # user_list = User.query.filter(or_(User.username.contains('z'), User.username.endswith('z'))).all()   #或者
    # user_list = User.query.filter(and_(User.username.startswith('x'), User.rdatetime > '2020-07-25')).all()  # 并且
    # User.query.filter(not_(User.username.contains('x'))).all()  # 不包含
    # User.query.filter(User.phone.in_(['12454', '2141'])).all()  # 在什么里面
    # User.query.filter(User.username.contains('x')).order_by(-User.username).all()  # 反序
    # User.query.limit(2).all()  # 获取前两条数据
    # User.query.offset(2).limit(2).all()  # 跳过两条数据再获取两条数据

    return render_template('base.html')


@user_bp.route('/myphoto')
def myphoto():
    photos = Photo.query.all()
    uid = session.get('uid', None)
    if uid:
        user = User.query.get(uid)
    else:
        user = None
    return render_template('user/myphoto.html', photos=photos, user=user, types=g.types)


@user_bp.route('/about_me', methods=['GET', 'POST'], endpoint='aboutme')
def aboutme():
    try:
        content = request.form.get('about')
        am = Aboutme()
        am.content = content.encode('utf-8')
        am.user_id = g.user.id
        db.session.add(am)
        db.session.commit()
    except Exception as err:
        redirect(url_for('user.center'))

    return render_template('user/aboutme.html', user=g.user, types=g.types)


@user_bp.route('/showme')
def showme():
    return render_template('user/aboutme.html', user=g.user, types=g.types)



@user_bp.route('/board')
def board():
    uid = session.get('uid')
    user = None
    if uid:
        user = User.query.get(uid)
    content = request.args.get('content')
    page = request.args.get('page',1)
    if content:
        board = Messageboard()
        board.user_id = uid
        board.content = content
        db.session.add(board)
        db.session.commit()
    board = Messageboard.query.order_by(-Messageboard.mdatetime).paginate(page=int(page), per_page=4)
    return render_template('user/board.html', types=g.types, user=user, board=board)

@user_bp.route('/del_message')
def del_message():
    bid = request.args.get('bid')
    message = Messageboard.query.filter(Messageboard.id == bid).first()
    db.session.delete(message)
    db.session.commit()
    return redirect(url_for('user.center'))

@user_bp.route('/checkphone')
def check_phone():
    phone = request.args.get('phone')
    user = User.query.filter(User.phone == phone).first()

    if user:
        return jsonify(code=400, msg='手机号码已存在')
    else:
        return jsonify(code=200, msg='手机号码可用')
