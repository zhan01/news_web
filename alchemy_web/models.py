from datetime import datetime
from alchemy_web import db, login_manager, ma
from flask_login import UserMixin


class BaseModel(db.Model):
    __abstract__ = True
    created_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, nullable=False,
                           default=datetime.utcnow)


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(BaseModel, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(20), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    image_file = db.Column(
        db.String(20), nullable=False, default='default.jpg')
    interests = db.relationship('Interest', backref='user', lazy=True)
# in user model refercing the interest class = upper case I

    def __repr__(self):
        return f"{self.username, self.email, self.image_file}"


class Interest(BaseModel):
    id = db.Column(db.Integer, primary_key=True)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
# in interest model user refers to table so lowercase u

    def __repr__(self):
        return f"{self.content , self.user_id}"

# Schema's from marshmallow for jsonify


class UserSchema(ma.ModelSchema):
    class Meta:
        model = User


class InterestSchema(ma.ModelSchema):
    class Meta:
        model = Interest


user_schema = UserSchema(strict=True)
users_schema = UserSchema(many=True, strict=True)

interest_schema = InterestSchema(strict=True)
interests_schema = InterestSchema(many=True, strict=True)
