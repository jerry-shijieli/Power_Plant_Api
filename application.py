from flask import Flask, jsonify, abort
from flask_restful import Resource, Api
from sqlalchemy import create_engine

app = Flask(__name__)
engine = create_engine('sqlite:///egrid2018_data.db')
api = Api(app)

class DisplayAllPlant(Resource):

    def get(self):
        """
        Retrieve all the plants with absolute values and percentage in its federal state
        """
        conn = engine.connect()
        query = conn.execute('SELECT out."eGRID2018 Plant file sequence number" AS id, out."Plant latitude" AS latitude, out."Plant longitude" AS longitude, ABS(out."Plant annual net generation (MWh)") AS abs_val, ABS(out."Plant annual net generation (MWh)")*100.0/ABS(tot.state_tot) AS state_percentage FROM PLNT18 AS out LEFT JOIN (SELECT SUM("Plant annual net generation (MWh)") AS state_tot, "Plant state abbreviation" FROM PLNT18 GROUP BY "Plant state abbreviation") AS tot ON out."Plant state abbreviation" = tot."Plant state abbreviation";')
        res = {'data' : [dict(zip(tuple(query.keys()), val)) for val in query.cursor]}
        print(res)
        return jsonify(res) if res['data'] else abort(204, 'No data found')


api.add_resource(DisplayAllPlant, '/allplants', endpoint='all_plants')

if __name__ == '__main__':
    app.run(port='5002', debug=True)