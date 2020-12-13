from db import db
from models.user import UserModel


class TeacherModel(UserModel):
    id = db.Column(db.Integer, db.ForeignKey(
        'user_model.id'), primary_key=True)
    allowed = db.Boolean(False)

    __mapper_args__ = {
        'polymorphic_identity': 'teacher',
    }

    def __init__(self, email, password, allowed=False):
        self.email = email
        self.password = password
        self.allowed = allowed

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    def json(self):
        return {
            'id': self.id,
            'email': self.email,
            'type': self.type,
            'allowed': "true" if self.allowed else "false"
        }

    @classmethod
    def find_all(cls):
        return cls.query.all()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
