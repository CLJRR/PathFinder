# from firebase_admin import credentials, initialize_app
from flask import Flask, redirect

import firebase_admin
from firebase_admin import credentials

cred = credentials.Certificate("api/serviceAccountKey.json")
firebase_admin.initialize_app(cred)
def create_app():
        app = Flask(__name__)
        app.config['SECRET_KEY'] = '12345678'
        from .userAPI import userAPI
        from .login import login
        from .employeeAPI import employeeAPI
        from .adminlogin import adminlogin
        from .mentorAPI import mentorAPI
        app.register_blueprint(userAPI,url_prefix='/user')
        app.register_blueprint(employeeAPI,url_prefix='/employeeDashboard')
        app.register_blueprint(login,url_prefix='/login')
        app.register_blueprint(adminlogin,url_prefix='/adminlogin')
        app.register_blueprint(mentorAPI,url_prefix='/mentor')
        @app.route('/')
        def redirect_to_login():
                return redirect('/login')
        return app