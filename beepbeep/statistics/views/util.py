import os
import mimetypes
import json
import urllib.request
from functools import update_wrapper
from datetime import timedelta
import requests
import time
import functools
from requests import RequestException

import yaml
from werkzeug.exceptions import HTTPException
from flask import jsonify, abort, current_app, request, make_response

def bad_response(code, message):
    return jsonify({'response-code': code, 'message': message}), code
