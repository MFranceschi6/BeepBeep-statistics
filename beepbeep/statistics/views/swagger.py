import os

from flakon import SwaggerBlueprint
from flask import request, jsonify
from sqlalchemy import and_
from datetime import datetime
from .util import bad_response, existing_user
import json
from json import loads

HERE = os.path.dirname(__file__)
YML = os.path.join(HERE, '..', 'static', 'api.yaml')
api = SwaggerBlueprint('API', __name__, swagger_spec=YML)


@api.operation('getAllStatisticsbyUserID')
def get_all_statistics_user_id(user_id):
    pass


