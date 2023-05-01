"""
This uses v2 api
https://learn.microsoft.com/en-us/azure/azure-functions/functions-reference-python?tabs=asgi%2Capplication-level&pivots=python-mode-decorators
"""

import azure.functions as func
import os
import time
import json

app = func.FunctionApp()

@app.function_name(name="get_last_update")
@app.route(route="last_update") # HTTP Trigger
def get_last_update(req: func.HttpRequest) -> func.HttpResponse:
    time_now_str = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    return func.HttpResponse(time_now_str)

@app.function_name(name="get_static")
@app.route(route="index")
def get_static(req: func.HttpRequest) -> func.HttpResponse:
    f = open(os.path.dirname(os.path.realpath(__file__)) + '/index/index.html')
    return func.HttpResponse(f.read(), mimetype='text/html')


@app.function_name(name="submit_news_form")
@app.route(route="submit_news_form") # HTTP Trigger
def submit_news_form(
        req: func.HttpRequest,
    ) -> func.HttpResponse:
    # receives a POST request with a JSON body and return a json response
    req_body = req.get_json()

    # json_response
    json_res = {"verbose": "Got response from the request."}

    if req_body:
        json_res["headlines"] = \
            f" Getting headlines for {req_body['category']}, {req_body['region']}, {req_body['length']} "

        return func.HttpResponse(
            body = json.dumps(json_res),
            status_code=200
        )
    else:
        json_res["verbose"] = "Error: No JSON body found in the request."
        return func.HttpResponse(
            body=json.dumps(json_res),
            status_code=400
        )
