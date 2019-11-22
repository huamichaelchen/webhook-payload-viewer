from flask import Flask, request, jsonify, redirect, url_for, session, render_template
from flask_pymongo import PyMongo
from pymongo import MongoClient
from healthcheck import HealthCheck, EnvironmentDump

import datetime
import bcrypt
import uuid
import os
import pymongo

# App configs
app = Flask(__name__)
app.config['MONGO_URI'] = os.environ.get('MONGO_URI')
app.config['MONGO_DBNAME'] = os.environ.get('MONGO_DBNAME')

# Initialization
connection = MongoClient(os.environ.get('MONGO_URI'))
database = connection[os.environ.get('MONGO_DBNAME')]
collection = database[os.environ.get('MONGO_DBNAME')]
mongo = PyMongo(app)
health = HealthCheck(app, "/healthcheck")
envdump = EnvironmentDump(app, "/environment")


@app.route('/', methods=['GET'])
def index():
    """

    :return: render the index.html page.
    """
    if 'username' in session:
        #return 'You are logged in as ' + session['username'] + ' and your access token is: ' + generate_access_token()
        return render_template('dashboard.html')
    return render_template('index.html')


@app.route('/register', methods=['POST', 'GET'])
def register():
    """

    :return: render register.html page. However, if after a POST request to register a user that's already existed, it
        will show a warning on the page.
    """
    if request.method == 'POST':
        users = mongo.db.users
        existing_user = users.find_one({'name': request.form['username']})

        if existing_user is None:
            hashpass = bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())
            users.insert({'name': request.form['username'], 'password': hashpass})
            session['username'] = request.form['username']
            return redirect(url_for('index'))

        return 'That username already exists!'

    return render_template('register.html')


@app.route('/login', methods=['POST'])
def login():
    """

    :return: redirect to index.html if login successful otherwise return a warning on the page.
    """
    users = mongo.db.users
    login_user = users.find_one({'name': request.form['username']})

    if login_user:
        if bcrypt.checkpw(request.form['pass'].encode('utf-8'),
                          bcrypt.hashpw(request.form['pass'].encode('utf-8'), bcrypt.gensalt())):
            session['username'] = request.form['username']
            return redirect(url_for('index'))

    return 'Invalid username/password combination'


# def generate_access_token():
#     return create_access_token(identity=session['username'])


@app.route('/svc', methods=['POST'])
def svc():
    """

    :return: Renders the webhook.html page
    """
    guid = generate_guid()
    collection.insert_one({"guid": guid,
                           "time": datetime.datetime.now(),
                           "user": session['username']})
    return render_template("webhook.html", guid=guid)


def generate_guid():
    """

    :return: a GUID like string
    """
    return str(uuid.uuid1())


@app.route('/mongodb_status')
def mongodb_status():
    """

    :return: mongodb server information in json format
    """
    return jsonify(connection.server_info()), 200


@app.route('/svc/guid/<string:guid>', methods=['GET', 'POST'])
def trigger_test_event(guid: str):
    """

    :param guid: the GUID string to be passed in
    :return:
        if HTTP 'GET' is called:
            return the latest record in the mongodb collection. This is to simulate latest updated Webhook event
        if HTTP 'POST' is called:
            return the updated record in raw string format. This is to simulate a Webhook event had happened. In this case
            it updated a record in MongoDB.
    """
    if request.method == 'GET':
        return str(collection.find().sort('$natural', pymongo.DESCENDING).limit(-1).next())
    if request.method == 'POST':
        payload = parse_request(request)
        return str(collection.find_one_and_update({'guid': guid}, {"$set": {"payload": payload}}))


def parse_request(req):
    """

    :param req: an HTTP request
    :return: Any response from the HTTP request regardless of the format
    """
    return req.get_data()


if __name__ == '__main__':
    app.secret_key = os.environ.get('SECRET')
    app.run(debug=True, host='0.0.0.0', use_reloader=True)
