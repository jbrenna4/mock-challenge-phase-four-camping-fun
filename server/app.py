from flask import Flask, request, make_response, jsonify
from flask_cors import CORS
from flask_migrate import Migrate
from flask_restful import Api, Resource

from models import db, Camper, Activity, Signup

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

api = Api(app)

CORS(app)
migrate = Migrate(app, db)

db.init_app(app)

# api = Api(app)


# @app.route('/')
# def index():
#     response = make_response(
#         {
#             "message": "Hello Campers!"
#         },
#         200
#     )
#     return response


# the get all for Campers
# we need our Post Campers here
class Campers(Resource):
    def get(self):
        camper_list = [camper.to_dict() for camper in Camper.query.all()]

        if not camper_list:
            make_response({'error: no camper list found'}, 404)

        else:
            response = make_response(camper_list, 200)

            return response

api.add_resource(Campers, '/campers')


# get campers by ID

class CampersById(Resource):
    def get(self):
        camper = Camper.query.filter(Camper.id == id).first().to_dict()

        if not camper:
            return make_response({"error: camper not found"}, 404)

        else:
            response = make_response(camper, 200)
            return response

api.add_resource =(CampersById, '/campers/<int:id>')

# GET /activities get all activities 
class Activities(Resource):
    def get(self):
        activity_list = [activity.to_dict() for activity in Activity.query.all()]
        
        if not activity_list:
            return make_response({"error: no activities found"}, 404)
        
        else: 
            response = make_response(activity_list, 200)
            return response
    
api.add_resource(Activities, '/activities')

# DELETE /activities/:id

class ActivityById(Resource):
    def get(self):

        activity = Activity.query.filter(Activity.id == id).first().to_dict()

        if not activity:
            return make_response({"error: activity not found"}, 404)

        else:
            db.session.delete(activity)
            db.session.commit()

            return make_response("delete was a success", 200)


# POST /signups
class Signups(Resource):
    def post(self):
        request_json = request.get_json()

        new_signup = Signup(
            time=request_json('time'),
            camper_id=request_json('camper_id'),
            activity_=request_json('activity_id'),
        )

        db.session.add(new_signup)
        db.session.commit()

        response = make_response(new_signup.to_dict(), 201)
        return response


if __name__ == '__main__':
    app.run(port=5555, debug=True)
