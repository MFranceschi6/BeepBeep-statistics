from flask import Blueprint
import os

static_file_dir = os.path.dirname(os.path.realpath(__file__))
home = Blueprint('home', __name__)


@home.route('/')
def some():
    return {'here': 1}


# @home.route('/api/<name>')
# @home.route('/api/<path>/<name>')
# def render_static(name, path=None):
#     print(static_file_dir+"/"+name)
#     if name == 'doc':
#         return send_from_directory(static_file_dir+"/../static/doc", 'index.html')
#     else:
#         if path is not None:
#             return send_from_directory(static_file_dir+"/../static/doc/"+path, name)
#         else:
#             return send_from_directory(static_file_dir + "/../static/doc", name)

