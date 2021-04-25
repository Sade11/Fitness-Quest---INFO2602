from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
db = SQLAlchemy()
import datetime


  
class Routine(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120),  nullable=False)
    start_date = db.Column(db.DateTime, default=datetime.datetime.utcnow) 

    def toDict(self):
        return{
            'id': self.id,
            'start_date': self.start_date.strftime("%m/%d/%Y, %H:%M:%S") 
        }
        
class CreateRoutines(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    routine_name = db.Column(db.String(120),  nullable=False)
    exercise_name = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(120),  nullable=False)
    day = db.Column(db.Integer, nullable=False)
    created = db.Column(db.DateTime, default=datetime.datetime.utcnow) 
    
    def toDict(self):
            return{
            'id':self.id,
            'routine_name':self.routine_name,
            'description':self.description,
            'day':self.day,
            'created': self.created.strftime("%m/%d/%Y, %H:%M:%S")
            }      

class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120),  nullable=False)
    video_url = db.Column( db.String(200))
    target_area = db.Column(db.String(200))

    def toDict(self):
        return{
        'id':self.id,
        'name':self.name,
        'video_url':self.video_url,
        'target_area':self.target_area
        }

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

    def toDict(self):
        return {
            "id": self.id,
            "username": self.username,
            "email": self.email,
            "password": self.password
        }

    def set_password(self, password):
        self.password = generate_password_hash(password, method='sha256')


    def check_password(self, password):
        return check_password_hash(self.password, password)

    def __repr__(self):
        return '<User {}>'.format(self.username)