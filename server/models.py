from flask_sqlalchemy import SQLAlchemy
from sqlalchemy_serializer import SerializerMixin
from sqlalchemy.orm import validates
from sqlalchemy.ext.associationproxy import association_proxy
from flask_restful import Resource


db = SQLAlchemy()


class Camper(db.Model, SerializerMixin):
    __tablename__ = 'campers'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    signups = db.relationship('Signup', back_populates='camper')

    @validates('name')
    def validate_name(self, key, name):
        if not name:
            raise ValueError('camper needs a name')
        return name
        
    @validates('age')
    def validate_age(self, key, age):
        if age < 7 or age > 19:
            raise ValueError('age must be between 8 and 18 years old')
        return age

    serialize_rules = ('-signups','-activities.campers', '-created_at', '-updated_at')

    def __repr__(self):
        return f'<Camper Name:{self.name}, Age:{self.age}, >'


class Activity(db.Model, SerializerMixin):
    __tablename__ = 'activities'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    difficulty = db.Column(db.Integer)
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    signups = db.relationship('Signup', back_populates='activity')

    serialize_rules = ('-signups.activity', '-camper.activities', '-created_at', '-updated_at')

    def __repr__(self):
        return f'<Activity Name:{self.name}, Difficulty:{self.difficulty},>'
    

class Signup(db.Model, SerializerMixin):
    __tablename__ = 'signups'

    id = db.Column(db.Integer, primary_key=True)
    time = (db.Integer) 
    created_at = db.Column(db.DateTime, server_default=db.func.now())
    updated_at = db.Column(db.DateTime, onupdate=db.func.now())

    camper_id = db.Column(db.Integer, db.ForeignKey('campers.id'))
    activity_id = db.Column(db.Integer, db.ForeignKey('activities.id'))

    serialize_rules = (('-camper.signups', '-activity.signups','-camper.activities', '-activity.campers','-created_at', '-updated_at'))

    camper = db.relationship('Camper', back_populates='signups')
    activity = db.relationship('Activity', back_populates='signups')

    @validates('time')
    def validate_time(self, key, time):
        if time < 0 or time > 23:
            raise ValueError('time must be between 0 and 23')
        return time


    # def __repr__(self):
    #     return f'<Activity Name:{self.name}, Difficulty:{self.difficulty},>'
