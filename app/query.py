from flask import Blueprint, request, jsonify
from utils.config import MONGO_DB, DIR_LIST, RET
import re

query = Blueprint('query', __name__, url_prefix='/word')


@query.route('/')
def query_word():
    """
    单词精确与模糊查询
    :return:
    """
    # 获取查询的单词字典{'w':'apple'}
    query_dict = request.args.to_dict()

    # 预处理,去除前后空格
    query_dict['w'] = query_dict['w'].strip()

    # 存储精确匹配的结果
    exact_list = []

    # 存储模糊匹配的结果
    fuzzy_list = []

    # 存储精确匹配的单词词性、释义
    tidy_exact = []

    # 存储模糊匹配的单词词性、释义
    tidy_fuzzy = []

    # 循环数据表列表,去库中每个单词数据表里检索单词
    for collection in DIR_LIST:
        # 精确匹配
        exact_res = MONGO_DB[collection].find_one(query_dict)
        if exact_res:
            # 当前表中查询到了单词
            exact_res.pop('_id')

            # 查询结果的释义和词性添加到字典中
            tidy_tmp_dict = {'w': exact_res.get('w'), 'bisp': exact_res.get('bisp')}

            # 如果此collection(单词表)查询到的结果并未重复
            if tidy_tmp_dict not in tidy_exact:

                # 将tidy_tmp_dict追加到列表中
                tidy_exact.append(tidy_tmp_dict)

                # 将单词字典添加到存储精确匹配的列表中
                exact_list.append(exact_res)

            # 只要表中查询到单词就将精确匹配列表中最后一项的(某表刚查询到的单词数据或前边已经查询到的重复的单词数据)添加分类
            exact_list[-1].setdefault('classification', []).append(collection)

        else:
            # 模糊匹配
            fuzzy_res = MONGO_DB[collection].find_one({'w': re.compile(query_dict.get('w'))})
            if fuzzy_res:
                fuzzy_res.pop('_id')

                # 将结果的释义和词性添加到字典中
                tidy_tmp_dict = {'w': fuzzy_res.get('w'), 'bisp': fuzzy_res.get('bisp')}

                # 如果此collection(单词表)查询到的结果并未重复
                if tidy_tmp_dict not in tidy_fuzzy:
                    tidy_fuzzy.append(tidy_tmp_dict)

                    # 将模糊查询的结果放到模糊匹配列表中
                    fuzzy_list.append(fuzzy_res)

                # 添加分类信息
                fuzzy_list[-1].setdefault('classification', []).append(collection)

    # 将精确、模糊查询结果合并
    res_list = exact_list + fuzzy_list
    tidy_res_list = tidy_exact + tidy_fuzzy

    if not res_list:
        RET['code'] = 29
        RET['msg'] = '未查询到单词'
        RET['data'] = {}
    else:
        RET['code'] = 30
        RET['msg'] = '查询结果列表'
        RET['data'] = {'res': res_list, 'tidy_res': tidy_res_list}
    return jsonify(RET)
