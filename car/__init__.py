from flask import Flask
from car.config import DevConfig
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_migrate import Migrate


app=Flask(__name__)

login_manager=LoginManager(app)




app.config.from_object(DevConfig)



db=SQLAlchemy(app)
migrate=Migrate(app,db)
from  car import views
login_manager.login_view='Login'