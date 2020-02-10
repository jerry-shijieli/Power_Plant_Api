from flask import Flask, jsonify, abort
from flask_restful import Resource, Api
from sqlalchemy import create_engine

app = Flask(__name__)
engine = create_engine('sqlite:///egrid2018_data.db')
api = Api(app)

if __name__ == '__main__':
    app.run(port='5002', debug=True)