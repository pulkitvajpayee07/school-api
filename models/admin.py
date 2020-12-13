from db import db
from models.user import UserModel


class AdminModel(UserModel):
    __tablename___ = 'admin'
    id = db.Column(db.Integer, db.ForeignKey(
        'user_model.id'), primary_key=True)
    admin_detail = db.Column(db.String(30))

    __mapper_args__ = {
        'polymorphic_identity': 'admin',
    }

    def __init__(self, email, password, admin_detail):
        self.email = email
        self.password = password
        self.admin_detail = admin_detail

    def json(self):
        return {
            'id': self.id,
            'email': self.email,
            'type': self.type,
            'detail': self.admin_detail
        }

    def save_to_db(self):
        db.session.add(self)
        db.session.commit()

    @classmethod
    def find_by_email(cls, email):
        return cls.query.filter_by(email=email).first()

    @classmethod
    def find_by_id(cls, id):
        return cls.query.filter_by(id=id).first()
