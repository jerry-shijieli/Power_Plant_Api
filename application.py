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

class DisplayTopPlant(Resource):

    def get(self, N):
        """
        Rank and retrieve the top N plants by the annual net generation.
        """
        if int(N) <= 0:
            return abort(400, 'Parameter is invalid')
        topN = int(N)
        conn = engine.connect()
        query = conn.execute('SELECT "eGRID2018 Plant file sequence number" AS id, "Plant latitude" AS latitude, "Plant longitude" AS longitude, "Plant annual net generation (MWh)" AS annua_net_generation FROM PLNT18 WHERE "Plant annual net generation (MWh)" <> "" ORDER BY "Plant annual net generation (MWh)" DESC LIMIT %d ;' % topN)
        res = {'data': [dict(zip(tuple(query.keys()), val)) for val in query.cursor]}
        print(res)
        return jsonify(res)  if res['data'] else abort(204, 'No data found')

class FilterPlantByState(Resource):

    def get(self, state_abbr):
        """
        Filter plants by its state abbreviation.
        """
        if len(state_abbr) != 2 or not state_abbr.isalpha():
            return abort(400, 'State abbreviation is required')
        conn = engine.connect()
        query = conn.execute('SELECT "eGRID2018 Plant file sequence number" AS id, "Plant latitude" AS latitude, "Plant longitude" AS longitude, "Plant annual net generation (MWh)" AS annua_net_generation, "Plant state abbreviation" AS state_abbr FROM PLNT18 WHERE "Plant annual net generation (MWh)" <> "" AND "Plant state abbreviation"  = "%s" ;' % state_abbr)
        res = {'data': [dict(zip(tuple(query.keys()), val)) for val in query.cursor]}
        print(res)
        return jsonify(res)  if res['data'] else abort(204, 'No data found')

api.add_resource(DisplayAllPlant, '/allplants', endpoint='all_plants')
api.add_resource(DisplayTopPlant, '/topnplants/<int:N>', endpoint='top_n_plants')
api.add_resource(FilterPlantByState, '/plantsbystate/<string:state_abbr>', endpoint='plants_by_state')

if __name__ == '__main__':
    app.run(port='5002', debug=True)