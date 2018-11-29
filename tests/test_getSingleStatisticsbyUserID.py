from unittest import mock
from requests.exceptions import RequestException
import pytest
from .fake_run_factory import FakeRunFactory


def test_getSingleStatisticsbyUserID_status_code_404(client):
    with mock.patch('beepbeep.statistics.views.swagger.requests') as mocked:
        mocked.get.return_value.status_code = 404
        response = client.get('/users/1/statistics/distances/')

        print(response.status_code)
        assert response.status_code == 404


def test_getSingleStatisticsbyUserID_status_code_503(client):
    with mock.patch('beepbeep.statistics.views.swagger.requests.get', side_effect=RequestException):
        response = client.get('/users/1/statistics/distances/')

        print(response.status_code)
        assert response.status_code == 503



def test_getSingleStatisticsbyUserID_status_code_400(client):
    with mock.patch('beepbeep.statistics.views.swagger.requests') as mocked:
        mocked.get.return_value.status_code = 200

        responses = []

        responses.append(client.get('/users/1/statistics/random_string/'))
        responses.append(client.get('/users/1/statistics/_distances_/'))
        responses.append(client.get('/users/1/statistics/distances_/'))
        responses.append(client.get('/users/1/statistics/_distances/'))

        for response in responses:
            assert response.status_code == 400


def send_requests(client):
    responses = dict()

    responses['distances'] = client.get('/users/1/statistics/distances/')
    responses['average_speeds'] = client.get('/users/1/statistics/average_speeds/')
    responses['average_heart_rates'] = client.get('/users/1/statistics/average_heart_rates/')
    responses['elevation_gains'] = client.get('/users/1/statistics/elevation_gains/')
    responses['elapsed_times'] = client.get('/users/1/statistics/elapsed_times/')

    for _, response in responses.items():
        assert response.status_code == 200

    return responses


def check_responses(responses, runFactory):
    for key, response in responses.items():
        assert response.json == {
            key: runFactory.stats[key],
            'run_names': runFactory.stats['run_names'],
            'run_ids': runFactory.stats['run_ids']}


@pytest.fixture
def test_getSingleStatisticsbyUserID_status_code_200(client):
    with mock.patch('beepbeep.statistics.views.swagger.requests') as mocked:
        mocked.get.return_value.status_code = 200

        yield send_requests(client)


def test_getSingleStatisticsbyUserID_no_runs(test_getSingleStatisticsbyUserID_status_code_200):
    responses = test_getSingleStatisticsbyUserID_status_code_200

    runFactory = FakeRunFactory()

    for key, response in responses.items():
        print(response.json)
        assert response.json == {
            key: runFactory.stats[key],
            'run_names': runFactory.stats['run_names'],
            'run_ids': runFactory.stats['run_ids']}



def _test_runs(client, n):
    with mock.patch('beepbeep.statistics.views.swagger.requests') as mocked:
        mocked.get.return_value.status_code = 200

        runFactory = FakeRunFactory()
        runFactory(n)
        mocked.get.return_value.json.return_value = runFactory.runs

        responses = send_requests(client)
        check_responses(responses, runFactory)


def test_getSingleStatisticsbyUserID_a_run(client):
    _test_runs(client, 1)

def test_getSingleStatisticsbyUserID_100_runs(client):
    _test_runs(client, 100)
