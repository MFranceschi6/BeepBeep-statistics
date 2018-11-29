from unittest import mock
from requests.exceptions import RequestException
import pytest
from .fake_run_factory import FakeRunFactory


def test_getAllStatisticsbyUserID_status_code_404(client):
    with mock.patch('beepbeep.statistics.views.swagger.requests') as mocked:
        mocked.get.return_value.status_code = 404
        response = client.get('/users/1/statistics/')

        print(response.status_code)
        assert response.status_code == 404


def test_getAllStatisticsbyUserID_status_code_503(client):
    with mock.patch('beepbeep.statistics.views.swagger.requests.get', side_effect=RequestException):
        response = client.get('/users/1/statistics/')

        print(response.status_code)
        assert response.status_code == 503



@pytest.fixture
def test_getAllStatisticsbyUserID_status_code_200(client):
    with mock.patch('beepbeep.statistics.views.swagger.requests') as mocked:
        mocked.get.return_value.status_code = 200
        response = client.get('/users/1/statistics/')

        print(response.status_code)
        assert response.status_code == 200

        yield response


def test_getAllStatisticsbyUserID_no_runs(test_getAllStatisticsbyUserID_status_code_200):
    json_response = test_getAllStatisticsbyUserID_status_code_200.json
    assert json_response == FakeRunFactory().stats



def _test_runs(client, n):
    with mock.patch('beepbeep.statistics.views.swagger.requests') as mocked:
        mocked.get.return_value.status_code = 200

        runFactory = FakeRunFactory()
        runFactory(n)

        mocked.get.return_value.json.return_value = runFactory.runs
        response = client.get('/users/1/statistics/')

        print(response.status_code)
        assert response.status_code == 200

        assert response.json == runFactory.stats


def test_getAllStatisticsbyUserID_a_run(client):
    _test_runs(client, 1)

def test_getAllStatisticsbyUserID_100_runs(client):
    _test_runs(client, 1)