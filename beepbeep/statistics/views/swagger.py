from flakon import SwaggerBlueprint
from .util import *



requests.adapters.DEFAULT_RETRIES = 7



HERE = os.path.dirname(__file__)
YML = os.path.join(HERE, '..', 'static', 'api.yaml')
api = SwaggerBlueprint('API', __name__, swagger_spec=YML)


DATA_SERVICE = 'http://'+os.environ['DATA_SERVICE']+':5002' if 'DATA_SERVICE' in os.environ else "http://127.0.0.1:5002"


@api.operation('getAllStatisticsbyUserID')
def get_all_statistics_user_id(user_id):
    #firstly check if the passed user_id actually exists

    try:
        url_request_user = requests.get(url=DATASERVICE_PATH + "/users/" + user_id)

        if (url_request_user.status_code == 404):
            return bad_response(404, "User not found for the user ID supplied.")

    except requests.exceptions.RequestException:
        return bad_response(503, "The 'dataservice' microservice on which this application depends on is not available."\
                                "Please, try again later.")


    #fine, we now have valid user ID.
    #we need to get the runs of the user
    url_request_runs = requests.get(url=DATASERVICE_PATH + "/users/" + user_id + "/runs")

    #process every single run for a user
    runs_response = url_request_runs.json()

    run_names_array = []
    run_ids_array = []
    distance_array = []
    average_speed_array = []
    average_heart_rate_array = []
    elevation_gain_array = []
    elapsed_time_array = []

    for run_response in runs_response:
        for attr in run_response:
            attr_value = run_response[attr]

            #if an attribute is found to have an invalid value, it is set to 0 to avoid wrong displays in the webservice JS
            if(attr_value == None or attr_value == "" or attr_value == "Null" or attr_value == "null"):
                attr_value = 0

            if(attr == "distance" ):
                distance_array.append(attr_value)
            #if invalid distance:
            elif(attr == "average_speed" ):
                average_speed_array.append(attr_value)
            elif(attr == "average_heartrate"):
                average_heart_rate_array.append(attr_value)
            elif(attr == "total_elevation_gain" ):
                elevation_gain_array.append(attr_value)
            elif(attr == "elapsed_time" ):
                elapsed_time_array.append(attr_value)
            elif(attr == "title"):
                run_names_array.append(attr_value)
            elif(attr == "id"):
                run_ids_array.append(attr_value)


    dictionary_output_response = {"distances" : distance_array, "average_speeds" : average_speed_array,
                                "average_heart_rates": average_heart_rate_array, "elevation_gains": elevation_gain_array,
                                  "elapsed_times": elapsed_time_array, "run_names": run_names_array,
                                  "run_ids" : run_ids_array }

    return jsonify(dictionary_output_response)



@api.operation('getSingleStatisticsbyUserID')
def get_single_statistics_user_id(user_id, statistics_name):

    try:
        statistics_name = str(statistics_name)
    except:
        return bad_response(400, "Invalid Statistics name type provided " + str(type(statistics_name)) + \
                                ". A valid string must be provided. ")

    # firstly, make sure a valid statistics name is being passed
    if not (statistics_name == "distances" or statistics_name == "average_speeds" or statistics_name == "average_heart_rates"
            or statistics_name == "elevation_gains" or statistics_name == "elapsed_times"):
        return bad_response(400, "Invalid Statistics name supplied: " + str(statistics_name) + ". A valid statistics name is" \
                             ": 'distances'|'average_speeds'|'average_heart_rates'|'elevation_gains'|'elapsed_times'. ")

    #firstly check if the passed user_id actually exists
    try:
        url_request_user = requests.get(url=DATASERVICE_PATH + "/users/" + user_id)

        if (url_request_user.status_code == 404):
            return bad_response(404, "User not found for the user ID supplied.")

    except requests.exceptions.RequestException:
        return bad_response(503,
                            "The 'dataservice' microservice on which this application depends on is not available."\
                            "Please, try again later.")


    #fine, we now have a valid user ID and a valid statistics ID
    #we need to get the runs of the user
    url_request_runs = requests.get(url=DATASERVICE_PATH + "/users/" + user_id + "/runs")

    #process every single run for a user
    runs_response = url_request_runs.json()

    run_names_array = []
    run_ids_array = []
    distance_array = []
    average_speed_array = []
    average_heart_rate_array = []
    elevation_gain_array = []
    elapsed_time_array = []

    #add the corresponding runs' statistics seeked to a dictionary
    for run_response in runs_response:
        for attr in run_response:
            attr_value = run_response[attr]

            if (attr_value == None or attr_value == "" or attr_value == "Null" or attr_value == "null"):
                attr_value = 0

            if(attr == "distance" and statistics_name == "distances" ):
                distance_array.append(attr_value)
            elif(attr == "average_speed" and statistics_name == "average_speeds" ):
                average_speed_array.append(attr_value)
            elif(attr == "average_heartrate" and statistics_name == "average_heart_rates"):
                average_heart_rate_array.append(attr_value)
            elif(attr == "total_elevation_gain" and statistics_name == "elevation_gains" ):
                elevation_gain_array.append(attr_value)
            elif(attr == "elapsed_time" and statistics_name == "elapsed_times"):
                elapsed_time_array.append(attr_value)
            elif (attr == "title"):
                run_names_array.append(attr_value)
            elif (attr == "id"):
                run_ids_array.append(attr_value)

    output_dictionary = {}

    if statistics_name == "distances":
        output_dictionary = {"distances" : distance_array}
    elif statistics_name == "average_speeds":
        output_dictionary = {"average_speeds" : average_speed_array}
    elif statistics_name == "average_heart_rates":
        output_dictionary = {"average_heart_rates": average_heart_rate_array}
    elif statistics_name == "elevation_gains":
        output_dictionary = {"elevation_gains": elevation_gain_array}
    elif statistics_name == "elapsed_times":
        output_dictionary = {"elapsed_times": elapsed_time_array}


    output_dictionary.update({"run_names" : run_names_array})

    output_dictionary.update({"run_ids" : run_ids_array})

    return jsonify(output_dictionary)
