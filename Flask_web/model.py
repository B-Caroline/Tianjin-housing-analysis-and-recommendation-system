from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

#定义数据库house_data_cleaning表的映射模型
class house_data_cleaning(db.Model):
    house_Introduce = db.Column(db.String, primary_key = True)
    house_Region = db.Column(db.String)
    house_Address = db.Column(db.String)
    house_Type = db.Column(db.String)
    house_Area = db.Column(db.String)
    house_floor = db.Column(db.String)
    house_Direction = db.Column(db.String)
    house_Price = db.Column(db.Integer)
    house_Heating = db.Column(db.String)
    house_Lease = db.Column(db.String)

#定义数据库user表的映射模型
class User(db.Model):
    account = db.Column(db.String, primary_key=True)
    password = db.Column(db.String)