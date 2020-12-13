from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims

from models.teacher import TeacherModel
from models.user import UserModel

help = "This field cannot be blank"
_teacher_parser = reqparse.RequestParser()
_teacher_parser.add_argument('email', type=str, required=True, help=help)
_teacher_parser.add_argument('password', type=str, required=True, help=help)
_teacher_parser.add_argument('allowed', type=bool, required=False)


class TeacherRegister(Resource):
    def post(self):
        data = _teacher_parser.parse_args()

        if TeacherModel.find_by_email(data['email']):
            return {"message": "User already registered"}, 400

        teacher = TeacherModel(**data)
        teacher.save_to_db()

        return {"message": "User created successfully"}, 201


class Teacher(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=False, help=help)
    parser.add_argument('password', type=str, required=False, help=help)
    parser.add_argument('allowed', type=bool, required=False, help=help)

    def get(self, id):
        teacher = TeacherModel.find_by_id(id)
        if not teacher:
            return {"message": "Teacher not found"}, 404
        return teacher.json(), 200

    def delete(self, id):
        teacher = TeacherModel.find_by_id(id)
        if not teacher:
            return {'messsage': 'Teacher not found'}, 404
        teacher.delete_from_db()
        return {'message': 'Teacher deleted.'}, 200

    @jwt_required
    def put(self, id):
        user = UserModel.find_by_id(get_jwt_identity())
        if not user:
            return {"message": "not authenticated"}, 401
        claims = get_jwt_claims()
        if not (claims['type'] == 'admin' or user.id == id or (claims['type'] == 'teacher' and user.allowed == True)):
            return {"message": "not authenticated"}, 401

        data = Teacher.parser.parse_args()
        teacher = TeacherModel.find_by_id(id)
        if not teacher:
            return {"message": "Teacher not found."}, 404
        if data['email'] is not None:
            teacher.email = data['email']
        if data['password'] is not None:
            teacher.password = data['password']
        if claims['type'] == 'admin' and data['allowed'] is not None:
            teacher.allowed = data['allowed']
        teacher.save_to_db()
        return {"message": "Teacher details updated"}, 200


class TeacherList(Resource):
    def get(self):
        return {'teachers': [x.json() for x in TeacherModel.find_all()]}
