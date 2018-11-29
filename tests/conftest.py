from beepbeep.statistics.app import create_app
import pytest
import os


@pytest.fixture
def app():
    app = create_app()
    app.config['TESTING'] = True

    yield app


@pytest.fixture
def client(app):
    client = app.test_client()

    yield client
