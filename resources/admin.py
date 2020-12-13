from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims

from models.admin import AdminModel
from models.teacher import TeacherModel

help = "This field cannot be blank"


class AdminRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help=help)
    parser.add_argument(
        'password', type=str, required=True, help=help)
    parser.add_argument('detail', dest='admin_detail',
                        type=str, required=True, help=help)

    def post(self):
        data = AdminRegister.parser.parse_args()

        if AdminModel.find_by_email(data['email']):
            return {"message": "User already registered"}, 400

        admin = AdminModel(**data)
        admin.save_to_db()

        return {"message": "User created successfully"}, 201


class ChangePermission(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('teacher_id', dest='id', type=int,
                        required=True, help=help)
    parser.add_argument('allowed', type=bool, required=True, help=help)

    @jwt_required
    def post(self):
        claims = get_jwt_claims()
        if claims['type'] != 'admin':
            return {"message": "Not authorized."}, 401
        data = ChangePermission.parser.parse_args()
        teacher = TeacherModel.find_by_id(data['id'])
        if not teacher:
            return {"message": "Teacher not found"}, 404
        teacher.allowed = claims['allowed']
        teacher.save_to_db()
        return {"message": "Permission updated."}, 200
