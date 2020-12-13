from flask import Flask
from flask_restful import Api
from flask_jwt_extended import JWTManager

from db import db
from models.admin import AdminModel
from models.teacher import TeacherModel
from models.user import UserModel

from resources.student import StudentRegister, StudentList, Student
from resources.teacher import TeacherRegister, TeacherList, Teacher
from resources.user import UserLogin, User, UserList
from resources.admin import AdminRegister

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'pulkit'
api = Api(app)


@app.before_first_request
def create_tables():
    db.create_all()


jwt = JWTManager(app)


@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    user = UserModel.find_by_id(identity)
    return {'type': user.type}


api.add_resource(StudentRegister, '/student')
api.add_resource(Student, '/student/<int:id>')
api.add_resource(StudentList, '/students')
api.add_resource(TeacherRegister, '/teacher')
api.add_resource(Teacher, '/teacher/<int:id>')
api.add_resource(TeacherList, '/teachers')
api.add_resource(AdminRegister, '/admin')
api.add_resource(User, '/user/<int:id>')
api.add_resource(UserList, '/users')
api.add_resource(UserLogin, '/login')

if __name__ == '__main__':
    db.init_app(app)
    app.run(port=5000, debug=True)
