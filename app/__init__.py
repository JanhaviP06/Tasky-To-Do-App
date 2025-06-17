from flask import Flask
from flask_sqlalchemy import SQLAlchemy #interact with db using python

#create database object globally
db=SQLAlchemy()

#appfactory
def create_app():
    app=Flask(__name__) #create flask app
     
    
    app.config['SECRET_KEY']='your-secret-key'
    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///todo.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

    #link db with app
    db.init_app(app)


    #modules are registered
    from app.routes.auth import auth_bp
    from app.routes.tasks import tasks_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(tasks_bp)

    return app
