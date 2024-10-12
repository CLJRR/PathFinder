from flask import Blueprint,request,jsonify, render_template
from firebase_admin import firestore

db = firestore.client()
user_Ref = db.collection("managers")
login = Blueprint("adminlogin",__name__)
