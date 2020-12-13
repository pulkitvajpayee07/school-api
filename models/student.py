from db import db
from models.user import UserModel


class StudentModel(UserModel):
    id = db.Column(db.Integer, db.ForeignKey(
        'user_model.id'), primary_key=True)
    course = db.Column(db.String(20))

    __mapper_args__ = {
        'polymorphic_identity': 'student',
    }

    def __init__(self, email, password, course):
        self.email = email
        self.password = password
        self.course = course

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def delete_from_db(self):
        db.session.delete(self)
        db.session.commit()

    def json(self):
        return {
            'id': self.id,
            'email': self.email,
            'type': self.type,
            'course': self.course
        }

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()
