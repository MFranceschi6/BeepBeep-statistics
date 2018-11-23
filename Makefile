HERE = $(shell pwd)
VENV = .
VIRTUALENV = virtualenv
BIN = $(VENV)/bin
PYTHON = $(BIN)/python
API=api.yaml
SERVICE=statistics

INSTALL = $(BIN)/pip install --no-deps

.PHONY: all test

all: build

$(PYTHON):
	$(VIRTUALENV) $(VTENV_OPTS) $(VENV)

build: $(PYTHON)
	$(PYTHON) setup.py develop

clean:
	rm -rf $(VENV)

test_dependencies:
	$(BIN)/pip install flake8 tox

test: build test_dependencies
	$(BIN)/tox

run:
	FLASK_APP=dataservice/app.py flask run

doc_dependencies:
	curl -sL https\://deb.nodesource.com/setup_8.x | sudo bash - && apt-get install nodejs bundler

slate:
	git clone https\://github.com/MFranceschi6/slate.git

widdershins: slate
	widdershins --expandBody ./$(PKG)/$(SERVICE)/static/$(API) -o ./slate/source/index.html.md

build_middleman: slate
ifeq ($(shell  gem list \^middleman\$$ -i),false)
	cd ./slate && bundle install
endif

build_docs: widdershins build_middleman
	cd ./slate && bundle exec middleman build

create_static:
	mkdir -p src/flakon/flakon/static

create_static_doc: create_static
	mkdir -p src/flakon/flakon/static/doc/

create_docs:
	mkdir -p docs

docs: widdershins build_docs create_static_doc create_docs
	cd ./slate && cp -r build/* ../src/flakon/flakon/static/doc/ && cp -r build/* ../docs/

clean-doc-env:
	rm  -rf slate

clean-doc:
	rm -rf docs && rm -rf src/flakon/flakon/static

dirtree:
	mkdir -p beepbeep/$(SERVICE) beepbeep/$(SERVICE)/static beepbeep/$(SERVICE)/tests beepbeep/$(SERVICE)/views beepbeep/$(SERVICE)

setupp:
	echo "from setuptools import setup, find_packages\n\
	from beepbeep.dataservice import __version__\n\
	\n\
	\n\
	setup(name='beepbeep-data',\n\
		version=__version__,\n\
		packages=find_packages(),\n\
		include_package_data=True,\n\
		zip_safe=False,\n\
		entry_points=\"\"\"\n\
		[console_scripts]\n\
		beepbeep-$(SERVICE) = beepbeep.$(SERVICE).run:main\n\
		\"\"\")" > setup.py

requirements:
	echo "pyjwt\n\
	-e git+https://github.com/MFranceschi6/flakon.git#egg=flakon\n\
	flask_webtest\n\
	cryptography\n\
	sqlalchemy\n\
	flask_sqlalchemy\n\
	chaussette\n\
	flask_cors" > requirements.txt

beepbeep-init:
	echo "from pkgutil import extend_path\n\
	__path__ = extend_path(__path__, __name__)" > beepbeep/__init__.py

service-init:
	echo "\n\
	__version__ = '0.1'" > beepbeep/$(SERVICE)/__init__.py

service-run:
	echo "import argparse\n\
	import sys\n\
	import signal\n\
	\n\
	from chaussette.server import make_server\n\
	from werkzeug.serving import run_with_reloader\n\
	\n\
	from beepbeep.dataservice.app import create_app\n\
	from beepbeep.dataservice.database import db, init_database\n\
	\n\
	\n\
	def _quit(signal, frame):\n\
		print(\"Bye!\")\n\
		# add any cleanup code here\n\
		sys.exit(0)\n\
	\n\
	\n\
	def main(args=sys.argv[1:]):\n\
		parser = argparse.ArgumentParser(description='beepbeep Dataservice')\n\
	\n\
		parser.add_argument('--fd', type=int, default=None)\n\
		parser.add_argument('--config-file', help='Config file',\n\
							type=str, default=None)\n\
		args = parser.parse_args(args=args)\n\
	\n\
		app = create_app(args.config_file)\n\
		host = app.config.get('host', '0.0.0.0')\n\
		port = app.config.get('port', 5000)\n\
		debug = app.config.get('DEBUG', False)\n\
	\n\
		signal.signal(signal.SIGINT, _quit)\n\
		signal.signal(signal.SIGTERM, _quit)\n\
	\n\
		db.init_app(app)\n\
		db.app = app\n\
		db.create_all(app=app)\n\
		init_database()\n\
	\n\
		if args.fd is not None:\n\
			# use chaussette\n\
			httpd = make_server(app, host='fd://%d' % args.fd)\n\
			httpd.serve_forever()\n\
		else:\n\
			app.run(debug=debug, host=host, port=port, use_reloader=debug)\n\
	\n\
	\n\
	if __name__ == \"__main__\":\n\
		main()\n\
	" > beepbeep/$(SERVICE)/run.py

service-settings:
	echo "[flask]\n\
	DEBUG = 1\n\
	SQLALCHEMY_TRACK_MODIFICATIONS = False\n\
	SQLALCHEMY_DATABASE_URI = sqlite:////tmp/beepbeep.$(SERVICE).db\n\
	NEED_TOKEN = False\n\
	pub_key = ${TESTDIR}/pubkey.pem\n\
	host = 127.0.0.1\n\
	port = 5002\n\
	" > beepbeep/$(SERVICE)/settings.ini

service-app:
	echo "import os\n\
from werkzeug.exceptions import HTTPException\n\
from flakon import create_app as _create_app\n\
from flakon.util import error_handling\n\
from flask import request, abort, g\n\
from flask_cors import CORS\n\
\n\
import jwt\n\
\n\
from .views import blueprints\n\
from .database import db\n\
\n\
\n\
_HERE = os.path.dirname(__file__)\n\
os.environ['TESTDIR'] = os.path.join(_HERE, 'tests')\n\
_SETTINGS = os.path.join(_HERE, 'settings.ini')\n\
\n\
\n\
def create_app(settings=None):\n\
    if settings is None:\n\
        settings = _SETTINGS\n\
\n\
    app = _create_app(blueprints=blueprints, settings=settings)\n\
\n\
    with open(app.config['pub_key']) as f:\n\
        app.config['pub_key'] = f.read()\n\
\n\
    CORS(app)\n\
\n\
    @app.before_request\n\
    def before_req():\n\
        if app.config.get('NEED_TOKEN', True):\n\
            authenticate(app, request)\n\
\n\
    return app\n\
\n\
\n\
def _400(desc):\n\
    exc = HTTPException()\n\
    exc.code = 400\n\
    exc.description = desc\n\
    return error_handling(exc)\n\
\n\
\n\
def authenticate(app, request):\n\
    key = request.headers.get('Authorization')\n\
    if key is None:\n\
        return abort(401)\n\
\n\
    key = key.split(' ')\n\
    if len(key) != 2:\n\
        return abort(401)\n\
\n\
    if key[0].lower() != 'bearer':\n\
        return abort(401)\n\
\n\
    pub_key = app.config['pub_key']\n\
    try:\n\
        token = key[1]\n\
        token = jwt.decode(token, pub_key, audience='beepbeep.io')\n\
    except Exception as e:\n\
        return abort(401)\n\
\n\
    # we have the token ~ copied into the globals\n\
    g.jwt_token = token\n\
" > beepbeep/$(SERVICE)/app.py

service-view-init:
	echo "blueprints = []" > beepbeep/$(SERVICE)/views/__init__.py

project: dirtree setupp requirements beepbeep-init service-init service-run service-settings service-app service-view-init