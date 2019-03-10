from flask import Blueprint, request, jsonify
from utils.config import MONGO_DB, RET
from forms.forms import RegForm
from datetime import datetime
from uuid import uuid4

auth = Blueprint('auth', __name__, url_prefix='/auth')


@auth.route('/register', methods=['POST'])
def register():
    """
    用户注册
    :return:
    """
    # 获取POST请求提交的user,nick,pwd,re_pwd,email
    reg_form = request.form

    # 用户名
    user = reg_form.get('user')

    # 校验数据是否合法
    form_obj = RegForm(formdata=reg_form)
    if not form_obj.validate():
        RET['code'] = 21
        RET['msg'] = form_obj.errors
        RET['data'] = []
        return jsonify(RET)

    # 数据库中不存储re_pwd数据,故剔除re_pwd
    reg_form = reg_form.to_dict()
    reg_form.pop('re_pwd')

    # 检验用户名是否重复
    if MONGO_DB.users.find_one({'user': user}):
        RET['code'] = 1
        RET['msg'] = f'用户名:{user}已被注册,请重新输入用户名'
        RET['data'] = []
        return jsonify(RET)

    # 设置关联的单词表,默认为空列表
    reg_form['vocabulary'] = []

    # 设置默认的背诵单词记录
    reg_form['recite_record'] = []

    # 记录注册时间戳
    reg_form['reg_time'] = datetime.now()

    # 设置默认登录时间为空
    reg_form['login_time'] = datetime.now()

    # 设置默认token,
    reg_form['token'] = str(uuid4())

    # 将用户注册数据写入数据库
    MONGO_DB.users.insert_one(reg_form)

    RET['code'] = 2
    RET['msg'] = f'{user}注册成功,已自动登录'
    RET['data'] = {'token': reg_form.get('token'), 'nick': reg_form.get('nick'), 'user': reg_form.get('nick')}
    return jsonify(RET)


@auth.route('/login', methods=['POST'])
def login():
    """
    用户登录
    :return:
    """
    # 获取用户提交的user(或email)以及pwd,并转化成字典
    login_form = request.form.to_dict()

    # 根据用户名(或邮箱)和密码进行用户校验
    user_info = MONGO_DB.users.find_one(
        {'$or': [login_form, {'email': login_form.get('user'), 'pwd': login_form.get('pwd')}]})

    # 用户名或密码错误,登录失败
    if not user_info:
        RET['code'] = 3
        RET['msg'] = '用户名或密码错误,请重新输入'
        return jsonify(RET)

    # 更新登录标识token,以及登陆时间
    user_info['token'] = str(uuid4())
    user_info['login_time'] = datetime.now()

    # 数据库中更新用户登录状态
    MONGO_DB.users.update_one({'_id': user_info.get('_id')}, {'$set': user_info})

    # 登陆成功,返回token、昵称和用户名
    RET['code'] = 4
    RET['msg'] = '登陆成功,正在跳转'
    RET['data'] = {'token': user_info.get('token'), 'nick': user_info.get('nick'), 'user': user_info.get('user')}
    return jsonify(RET)


@auth.route('/logout', methods=['OPTIONS', 'POST'])
def logout():
    """
    用户注销
    :return:
    """
    # 放行预检请求
    if request.method == 'OPTIONS':
        return ''
    token = request.headers.get('Authorization')
    if token:
        MONGO_DB.users.update_one({'token': token}, {'$set': {'token': ''}})
        RET['code'] = 6
        RET['msg'] = '注销成功,正在跳转'
        RET['data'] = []
        return jsonify(RET)
