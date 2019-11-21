from flask import Flask, request, jsonify, redirect, url_for
from urllib.parse import unquote_plus
from pymongo import MongoClient
from flask_jwt_extended import JWTManager
from healthcheck import HealthCheck, EnvironmentDump

import json
import re
import uuid
import datetime
import os

# App configs
app = Flask(__name__)
app.config['MONGO_URI'] = os.environ.get('DB')
app.config['JWT_SECRET_KEY'] = os.environ.get('SECRET')
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = datetime.timedelta(days=1)


# Initialization
connection = MongoClient(os.environ.get('DB'))
jwt = JWTManager(app)
health = HealthCheck(app, "/healthcheck")
envdump = EnvironmentDump(app, "/environment")


@app.route('/', methods=['GET'])
def index():
    """
    Go to localhost:5000 and redirect to localhost:/svc
    """
    return redirect(url_for('svc'))


@app.route('/svc', methods=['GET'])
def svc():
    """
    Generate a GUID
    """
    return jsonify(webhook_endpoint="Here is your WebHook Location: http://localhost:5000/svc/" + generate_guid()), 200


def generate_guid():
    return str(uuid.uuid1())


@app.route('/svc/<string:guid>', methods=['GET', 'POST'])
def print_test(guid: str):
    """
    Send a POST request to localhost:5000/api/print with a JSON body with a "p" key
    to print that message in the server console.
    """
    payload = parse_request(request)
    print(payload)
    return (payload, 200, None)


def parse_request(req):
    """
    Parses application/json request body data into a Python dictionary
    """
    if req.headers['Content-Type'] == 'text/plain':
        return "Text Message: " + request.data

    elif req.headers['Content-Type'] == 'application/json':
        return "JSON Message: " + json.dumps(request.json)

    elif req.headers['Content-Type'] == 'application/octet-stream':
        f = open('./binary', 'wb')
        f.write(request.data)
        f.close()
        return "Binary message written!"
    else:
        return "415 Unsupported Media Type ;)"

    return payload


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', use_reloader=True)
