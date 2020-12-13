from flask_restful import Resource, reqparse
from flask_jwt_extended import get_jwt_identity, jwt_required, get_jwt_claims

from models.student import StudentModel
from models.user import UserModel

help = "This field cannot be blank"


class StudentRegister(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=True, help=help)
    parser.add_argument(
        'password', type=str, required=True, help=help)
    parser.add_argument('course', type=str, required=True, help=help)

    def post(self):
        data = StudentRegister.parser.parse_args()

        if StudentModel.find_by_email(data['email']):
            return {"message": "User already registered"}, 400

        student = StudentModel(**data)
        student.save_to_db()

        return {"message": "User created successfully"}, 201


class Student(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('email', type=str, required=False, help=help)
    parser.add_argument('password', type=str, required=False, help=help)
    parser.add_argument('course', type=str, required=False, help=help)

    def get(self, id):
        student = StudentModel.find_by_id(id)
        if not student:
            return {"message": "Student not found"}, 404
        return student.json(), 200

    def delete(self, id):
        student = StudentModel.find_by_id(id)
        if not student:
            return {'messsage': 'Student not found'}, 404
        student.delete_from_db()
        return {'message': 'Student deleted.'}, 200

    @jwt_required
    def put(self, id):
        user = UserModel.find_by_id(get_jwt_identity())
        if not user:
            return {"message": "not authenticated"}, 401
        claims = get_jwt_claims()
        if not (claims['type'] == 'admin' or user.id == id or (claims['type'] == 'teacher' and user.allowed == True)):
            return {"message": "not authenticated"}, 401
        data = Student.parser.parse_args()
        student = StudentModel.find_by_id(id)
        if not student:
            return {"message": "Student not found."}, 404
        if data['email'] is not None:
            student.email = data['email']
        if data['password'] is not None:
            student.password = data['password']
        if data['course'] is not None:
            student.course = data['course']
        student.save_to_db()
        return {"message": "Student detail updated"}, 200


class StudentList(Resource):
    def get(self):
        return {'students': [x.json() for x in StudentModel.find_all()]}
