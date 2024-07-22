from datetime import datetime

from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, Integer, String, Boolean, DateTime, func


db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    Fname = db.Column(db.String(80), unique=False, nullable=False)
    Lname = db.Column(db.String(80), unique=False, nullable=False)
    phone = db.Column(db.String(25), unique=False, nullable=False)
    email = db.Column(db.String(80), unique=False, nullable=False)
    b_date = db.Column(db.Date, unique=False, nullable=False)
    password = db.Column(db.String(500), nullable=False)

class Task(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), unique=False, nullable=True)
    isDone = db.Column(Boolean, unique=False, default=False)
    creation_date = db.Column(DateTime, default=func.now(),unique=False, nullable=False)
    execution_date = db.Column(db.Date, unique=False, nullable=False)




def db_update(table,column,value):
    return 0

    
# def db_delete():