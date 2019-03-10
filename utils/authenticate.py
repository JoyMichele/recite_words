from utils.config import RET, TOKEN_LIFETIME_DAYS, MONGO_DB
from datetime import datetime
from flask import jsonify


def authenticate(request):
    """
    验证是否登录的中间件
    :param request: 请求对象
    :return:
    """
    # 将预检请求放行
    if request.method == 'OPTIONS':
        return

    # 获取请求头中的token
    token = request.headers.get('Authorization')
    if not token:
        RET['code'] = 11
        RET['msg'] = 'token不合法'
        RET['data'] = []
        return jsonify(RET)

    # 根据token查询用户信息
    user_info = MONGO_DB.users.find_one({'t.oken': token})
    if not user_info:
        RET['code'] = 11
        RET['msg'] = 'token不合法'
        RET['data'] = []
        return jsonify(RET)

    # 判断token是否过期
    last_time = user_info.get('login_time')
    current_time = datetime.now()
    if (current_time - last_time).days > TOKEN_LIFETIME_DAYS:
        RET['code'] = 13
        RET['msg'] = 'token已过期'
        RET['data'] = []
        return jsonify(RET)
