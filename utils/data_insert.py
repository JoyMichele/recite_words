import os
import json
from utils.config import STATIC_FOLDER, MONGO_DB, DIR_LIST

# 获取单词分类目录
for dir_name in DIR_LIST:
    # 单词分类文件夹的名称
    dir_path = os.path.join(STATIC_FOLDER, dir_name)

    # 各单词分类下的单词文件列表
    file_list = os.listdir(dir_path)
    file_list.remove('summary.js')

    for file_name in file_list:
        # 各单词分类下的单词文件路径
        file_path = os.path.join(dir_path, file_name)
        with open(file_path, 'r', encoding='utf-8')as f:
            content = f.read()
            content = content.strip()[11:-2].strip(',') + ']'
            word_list = json.loads(content)
            MONGO_DB[dir_name].insert_many(word_list)
