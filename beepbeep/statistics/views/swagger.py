import os

from flakon import SwaggerBlueprint
from flask import jsonify
import json
from json import loads
import requests
from .util import *

requests.adapters.DEFAULT_RETRIES = 7



HERE = os.path.dirname(__file__)
YML = os.path.join(HERE, '..', 'static', 'api.yaml')
api = SwaggerBlueprint('API', __name__, swagger_spec=YML)


DATASERVICE_PATH="http://127.0.0.1:5002"


@api.operation('getAllStatisticsbyUserID')
def get_all_statistics_user_id(user_id):
    #firstly check if the passed user_id actually exists

    try:
        url_request_user = requests.get(url=DATASERVICE_PATH + "/users/" + user_id)

        if (url_request_user.status_code == 404):
            return bad_response(404, "User not found for the user ID supplied.")

    except requests.exceptions.RequestException:
        return bad_response(503, "The 'dataservice' microservice on which this application depends on is not available. Please, try again later.")


    #fine, we now have valid user ID.
    #we need to get the runs of the user
    url_request_runs = requests.get(url=DATASERVICE_PATH + "/users/" + user_id + "/runs")

    #process every single run for a user
    runs_response = url_request_runs.json()

    distance_array = []
    average_speed_array = []
    average_heart_rate_array = []
    elevation_gain_array = []
    elapsed_time_array = []

    for run_response in runs_response:
        for attr in run_response:
            if(attr == "distance"):
                distance_array.append(run_response[attr])
            elif(attr == "average_speed"):
                average_speed_array.append(run_response[attr])
            elif(attr == "average_heartrate"):
                average_heart_rate_array.append(run_response[attr])
            elif(attr == "total_elevation_gain"):
                elevation_gain_array.append(run_response[attr])
            elif(attr == "elapsed_time"):
                elapsed_time_array.append(run_response[attr])

    dictionary_output_response = {"distance_array" : distance_array, "average_speed_array" : average_speed_array,
                                "average_heart_rate_array": average_heart_rate_array, "elevation_gain_array": elevation_gain_array,
                                  "elapsed_time_array": elapsed_time_array}

    return jsonify(dictionary_output_response)



@api.operation('getSingleStatisticsbyUserID')
def get_single_statistics_user_id(user_id, statistics_id):

    try:
        statistics_id = int(statistics_id)
    except:
        return bad_response(400, "Invalid Statistics ID type provided " + str(type(statistics_id)) + ". An integer must be provided. ")

    #firstly, make sure a valid statistics ID is being passed
    if not 1 <= statistics_id <= 5:
        return bad_response(400, "Invalid Statistics ID supplied " + str(statistics_id) + ".A valid statistics ID is in the range [1, 5]. ")

    #firstly check if the passed user_id actually exists
    try:
        url_request_user = requests.get(url=DATASERVICE_PATH + "/users/" + user_id)

        if (url_request_user.status_code == 404):
            return bad_response(404, "User not found for the user ID supplied.")

    except requests.exceptions.RequestException:
        return bad_response(503,
                            "The 'dataservice' microservice on which this application depends on is not available. Please, try again later.")


    #fine, we now have a valid user ID and a valid statistics ID
    #we need to get the runs of the user
    url_request_runs = requests.get(url=DATASERVICE_PATH + "/users/" + user_id + "/runs")

    #process every single run for a user
    runs_response = url_request_runs.json()

    distance_array = []
    average_speed_array = []
    average_heart_rate_array = []
    elevation_gain_array = []
    elapsed_time_array = []

    #add the corresponding runs' statistics seeked to a dictionary
    for run_response in runs_response:
        for attr in run_response:
            if(attr == "distance" and statistics_id == 1):
                distance_array.append(run_response[attr])
            elif(attr == "average_speed" and statistics_id == 2):
                average_speed_array.append(run_response[attr])
            elif(attr == "average_heartrate" and statistics_id == 3):
                average_heart_rate_array.append(run_response[attr])
            elif(attr == "total_elevation_gain" and statistics_id == 4):
                elevation_gain_array.append(run_response[attr])
            elif(attr == "elapsed_time" and statistics_id == 5):
                elapsed_time_array.append(run_response[attr])

    output_dictionary = {}

    if statistics_id == 1:
        output_dictionary = {"distance_array" : distance_array}
    elif statistics_id == 2:
        output_dictionary = {"average_speed_array" : average_speed_array}
    elif statistics_id == 3:
        output_dictionary = {"average_heart_rate_array": average_heart_rate_array}
    elif statistics_id == 4:
        output_dictionary = {"elevation_gain_array": elevation_gain_array}
    elif statistics_id == 5:
        output_dictionary = {"elapsed_time_array": elapsed_time_array}

    return jsonify(output_dictionary)
