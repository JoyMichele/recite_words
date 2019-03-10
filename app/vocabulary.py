from flask.views import MethodView
from utils.config import MONGO_DB, FILES_LIST
from flask import Blueprint, request, jsonify
from utils.authenticate import authenticate
from bson import ObjectId
from utils.config import RET

voc = Blueprint('voc', __name__, url_prefix='/vocabulary')


@voc.before_request
def is_login():
    """
    校验登录状态
    :return:
    """
    ret = authenticate(request)
    return ret


@voc.route('/list')
def list_voc():
    """
    获取词汇分类列表
    :return:
    """
    RET['code'] = 22
    RET['msg'] = '词汇列表'
    RET['data'] = FILES_LIST
    return jsonify(RET)


class Vocabulary(MethodView):
    """
    获取个人单词本,背诵记录
    :param classification: 单词本所属类别
    :return:
    """

    # 获取单词本
    def get(self):
        voc_param = request.args.to_dict()

        # 根据请求头中的token查询到user表中的用户
        user_info = MONGO_DB.users.find_one({'token': request.headers.get('Authorization')})

        # 在用户信息中查询到单词本的id
        classification = voc_param.get('classification')

        for voc in user_info.get('vocabulary'):
            if classification in voc:
                # 存在单词本,获取单词本数据
                voc_info = MONGO_DB.vocabulary.find_one({'_id': ObjectId(voc[classification])})
                RET['code'] = 28
                RET['msg'] = f'{classification}单词本列表'
                RET['data'] = voc_info.get('words_list')
                return jsonify(RET)
        else:
            # 单词本为空
            RET['code'] = 29
            RET['msg'] = f'{classification}单词本为空'
            RET['data'] = []
        return jsonify(RET)

    # 添加单词到个人单词本中
    def put(self):
        # 获取客户端提交的单词本所属分类classification,以及待添加单单词本的单词word和单词数据word_detail
        voc_form = request.json

        # 根据请求头中的token查询到user表中的用户
        user_info = MONGO_DB.users.find_one({'token': request.headers.get('Authorization')})
        user_id = str(user_info.get('_id'))

        # 单词本所属用户
        voc_form['owner'] = user_id

        # 获取待更新的单词及单词详情
        new_word = voc_form.pop('word')
        word_detail = voc_form.pop('word_detail')

        # 获取单词本的分类
        classification = voc_form.get('classification')

        # 查询用户的此分类词汇单词本
        voc_info = MONGO_DB.vocabulary.find_one(voc_form)
        if not voc_info:
            # 此单词本不存在,创建该用户的此单词本
            voc_info = MONGO_DB.vocabulary.insert_one({
                'owner': user_id,
                'classification': classification,
                'words_list': [word_detail]
            })

            RET['code'] = 24
            RET['msg'] = f'创建单词本:{classification},添加单词:{new_word}成功'
            RET['data'] = [word_detail]

            # 在用户表中更新用户的单词本列表
            MONGO_DB.users.update_one({'_id': ObjectId(user_id)},
                                      {'$push': {'vocabulary': {classification: str(voc_info.inserted_id)}}})

        else:
            for detail in voc_info.get('words_list'):
                if detail.get('w') == new_word:
                    # 单词已存在,删除单词本中记录的此单词
                    MONGO_DB.vocabulary.update_one(voc_form, {'$pull': {'words_list': word_detail}})
                    words_list = voc_info.get('words_list')
                    words_list.remove(word_detail)

                    RET['code'] = 23
                    RET['msg'] = f'已将单词:{new_word}移出单词本:{classification}'
                    RET['data'] = words_list
                    return jsonify(RET)

            # 将新单词加入单词本
            MONGO_DB.vocabulary.update_one(voc_form, {'$push': {'words_list': word_detail}})
            words_list = voc_info.get('words_list')
            words_list.append(word_detail)

            RET['code'] = 26
            RET['msg'] = f'添加单词:{new_word}到单词表:{classification}'
            RET['data'] = words_list

        return jsonify(RET)


voc.add_url_rule('/', view_func=Vocabulary.as_view('vocabulary'))
