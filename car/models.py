from car import db,login_manager
from flask_login import UserMixin
 
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id)) 


class User(db.Model,UserMixin):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(255),nullable=False,unique=True)
    email=db.Column(db.String(255),nullable=False)
    password=db.Column(db.String(255),nullable=False)
    #foreign key
    cars=db.relationship('Car',backref='owner',lazy=True)
    def __repr__(self):
        return  'User {}'.format(self.name)

class Car(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    name=db.Column(db.String(255),nullable=False,unique=True)
    car_type=db.Column(db.String(255),nullable=False)
    hire_price=db.Column(db.Integer,nullable=False)

    image_url=db.Column(db.Text,nullable=False)
    
    owner_id=db.Column(db.Integer,db.ForeignKey('user.id'))

    def __repr__(self):
        return 'Car {}'.format(self.name)
    
    