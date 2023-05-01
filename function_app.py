"""
This uses v2 api
https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python?tabs=asgi%2Capplication-level&pivots=python-mode-decorators
"""

import datetime
import azure.functions as func
import logging
import os
import time
import json
from newsgpt import NewsGPT
from azure.cosmos import exceptions, CosmosClient, PartitionKey

# cosmos db impl
# https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/cosmos/azure-cosmos/samples/examples.py

app = func.FunctionApp()

##############################################################################


@app.function_name(name="get_last_update")
@app.route(route="last_update", auth_level=func.AuthLevel.ANONYMOUS)
def get_last_update(req: func.HttpRequest) -> func.HttpResponse:
    time_now_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    # TODO: get this last update time from the database
    return func.HttpResponse(time_now_str)

##############################################################################


@app.function_name(name="get_static")
@app.route(route="index", auth_level=func.AuthLevel.ANONYMOUS)
def get_static(req: func.HttpRequest) -> func.HttpResponse:
    f = open(os.path.dirname(os.path.realpath(__file__)) + '/index/index.html')
    return func.HttpResponse(f.read(), mimetype='text/html')

##############################################################################


@app.function_name(name="submit_news_form")
@app.route(route="submit_news_form", auth_level=func.AuthLevel.ANONYMOUS)
def submit_news_form(
    req: func.HttpRequest,
) -> func.HttpResponse:
    # receives a POST request with a JSON body and return a json response
    req_body = req.get_json()

    # json_response
    json_res = {"verbose": "Got response from the request."}

    if req_body:
        json_res["headlines"] = \
            f" Getting headlines for {req_body['category']}, {req_body['region']}, {req_body['length']} \n " \
            f" HA, I am still a work in progress."

        # TODO: get the headlines from the database

        return func.HttpResponse(
            body=json.dumps(json_res),
            status_code=200
        )
    else:
        json_res["verbose"] = "Error: No JSON body found in the request."
        return func.HttpResponse(
            body=json.dumps(json_res),
            status_code=400
        )

##############################################################################
# Cron job to update the database from langchain
# https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-timer?tabs=python-v2%2Cin-process&pivots=programming-language-python


# TODO: this isnt working, dunno why need further debugging
@app.function_name(name="mytimer")
@app.schedule(# cron 30 secs 
              schedule="*/30 * * * * *",
              arg_name="mytimer",
              run_on_startup=True) 
def test_function(mytimer: func.TimerRequest) -> None:
    logging.info('Python timer trigger function')
    # TODO: update the database from langchain
    _api_key = "700fa82411ad46069807d49abd48c7ad"
    _api_base = "https://newsgpt.openai.azure.com/"
    _api_type = 'azure'
    _api_version = '2022-12-01'
    _model_name = "text-davinci-003"

    newsgpt = NewsGPT(api_key=_api_key,
                      api_type=_api_type,
                      api_base=_api_base,
                      api_version=_api_version,
                      model_name=_model_name)
