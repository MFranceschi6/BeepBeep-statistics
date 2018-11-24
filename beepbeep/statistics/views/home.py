from flask import Blueprint
import os
#from flakon.util import send_request

static_file_dir = os.path.dirname(os.path.realpath(__file__))
home = Blueprint('home', __name__)


@home.route('/')
def render_static():
    return "Statistics Home sweet home."
