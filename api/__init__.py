# from firebase_admin import credentials, initialize_app
from flask import Flask

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("api/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
def create_app():
        app = Flask(__name__)
        app.config['SECRET_KEY'] = '12345678'
        from .userAPI import userAPI
        app.register_blueprint(userAPI,url_prefix='/user')
        app.register_blueprint(employeeAPI,url_prefix='/employeedashboard')
        return app