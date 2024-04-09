# main.py
import os
from flask import Flask
from app.config import LocalDevelopmentConfig
from app.database import db, jwt
from app.controllers import app as routes_app
from flask_cors import CORS
# from mail import send_email

def create_app():
    app = Flask(__name__, template_folder="templates")
    app.register_blueprint(routes_app)

    CORS(app, resources={r"/*":{'origins':"*"}})

    if os.getenv('ENV', "development") == "production":
        raise Exception("Currently no production config is setup.")
    else:
        print("Starting Local Development")
        app.config.from_object(LocalDevelopmentConfig)
    
    db.init_app(app)
    jwt.init_app(app) 

    return app

if __name__ == '__main__':
    app = create_app() 
    with app.app_context():
        db.create_all()  
    app.run(host='0.0.0.0', port=5000)
