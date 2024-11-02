from flask import Blueprint, request
from flask_restx import Api, Resource

api_blueprint = Blueprint('api_routes', __name__)
api = Api(api_blueprint)


@api.route('/users')
class Usuarios(Resource):
    def get(self):

        pass

@api.route('/users', methods=['POST']) 
class PostUsuarios(Resource):
    def post(self):
        pass
    