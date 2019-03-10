from flask import Blueprint, send_file
import os

down = Blueprint('download', __name__, url_prefix='/download', static_folder='../download')


@down.route('/')
def download():
    # 添加文件描述响应头Content-Disposition: attachment; filename=recite_words.apk
    return send_file(os.path.join(down.static_folder, 'recite_words.apk'), as_attachment=True)
