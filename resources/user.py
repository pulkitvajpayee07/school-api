from flask_restful import Resource, reqparse
from flask_jwt_extended import create_access_token

from models.user import UserModel

help = "This field cannot be blank."
_user_parser = reqparse.RequestParser()
_user_parser.add_argument('email', type=str, required=True, help=help)
_user_parser.add_argument('password', type=str, required=True, help=help)


class UserLogin(Resource):
    def post(self):
        data = _user_parser.parse_args()

        user = UserModel.find_by_email(data['email'])

        if user and user.password == data['password']:
            access_token = create_access_token(identity=user.id)
            return {
                'access_token': access_token
            }, 200

        return {"message": "Invalid Credentials"}, 401


class User(Resource):
    def get(self, id):
        user = UserModel.find_by_id(id)

        if not user:
            return {"message": "User not found"}, 404
        return user.json(), 200


class UserList(Resource):
    def get(self):
        return {'users': [x.json() for x in UserModel.find_all()]}
