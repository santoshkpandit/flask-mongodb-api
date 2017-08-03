#!flask/bin/python
import API_v1
from flask import Flask, request, json

#from flask_pymongo import PyMongo

app = Flask(__name__)


app.config['MONGO2_DBNAME'] = 'test'
app.config['MONGO2_HOST'] = 'localhost'

#mongodb = PyMongo(app, config_prefix='MONGO2')



# Set up blueprints for each API version
app.register_blueprint(API_v1.blueprint, url_prefix='/1.0')


if __name__ == '__main__':
    app.run(host='127.0.0.1', port=5001, debug=True, threaded=True)