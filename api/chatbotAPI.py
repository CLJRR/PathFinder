from flask import Blueprint,request,jsonify, render_template, redirect, url_for
from firebase_admin import firestore

db = firestore.client()
dbCollection = db.collection("employees")
chatbotAPI = Blueprint('chatbotAPI', __name__)



@chatbotAPI.route('/', methods=['GET'])
def show_form():
    return render_template('chatbot.html')