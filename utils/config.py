import pymongo
import os

# Mongodb相关配置
client = pymongo.MongoClient('127.0.0.1', 27017)
MONGO_DB = client['recite_words']

# RET响应对象配置
RET = {
    'code': 0,
    'msg': '',
    'data': []
}
# code状态码定义
# ------ 1-10 用户相关状态码 ------
# 1 -- 注册用户名重复
# 2 -- 注册成功
# 3 -- 登录用户名或密码输入错误
# 4 -- 登陆成功
# 5 -- 当前未登录任何用户

# ------ 11-20 用户相关状态码 ------
# 11 -- token不合法
# 13 -- token已过期
# 15 -- 未携带token

# ------ 21-30 数据相关状态码 ------
# 21 -- 提交数据不合法
# 22 -- 词汇列表
# 23 -- 已经添加过此单词
# 24 -- 创建单词本,添加单词成功
# 26 -- 添加单词到单词本
# 27 -- 此分类单词本未添加过单词
# 28 -- 单词本列表
# 29 -- 未查询到单词
# 30 -- 查询结果列表


# token相关设置
TOKEN_LIFETIME_DAYS = 7

# 项目根目录
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# 静态文件配置
STATIC_FOLDER = os.path.join(BASE_DIR, 'static')

# 静态文件目录列表
DIR_LIST = os.listdir(STATIC_FOLDER)

# title与name对应关系
FILES_LIST = [
    {'title': 'GRE词汇',
     'name': 'GRE',
     'count': 7318
     },
    {'title': '四级词汇',
     'name': 'CET4',
     'count': 3750
     },
    {'title': '六级词汇',
     'name': 'CET6',
     'count': 2087
     },
    {'title': '专四词汇',
     'name': 'TEM4',
     'count': 8594
     },
    {'title': '专八词汇',
     'name': 'TEM8',
     'count': 12613
     },
    {'title': '考研词汇',
     'name': 'UNGEE',
     'count': 5218
     },
    {'title': '托福词汇',
     'name': 'TOEFL',
     'count': 9322
     },
    {'title': '雅思词汇',
     'name': 'IELTS',
     'count': 3432
     },
    {'title': '高考词汇',
     'name': 'NCEE',
     'count': 3826
     }
]


# 环境配置类
class ProductionConfig:
    """
    生产环境
    """
    DEBUG = False
    TESTING = False
    # 使项目支持中文
    JSON_AS_ASCII = False


class DebugConfig(ProductionConfig):
    """
    调试环境
    """
    DEBUG = True


class TestingConfig(ProductionConfig):
    """
    测试环境
    """
    TESTING = True
