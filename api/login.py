from flask import Blueprint,request,jsonify, render_template, redirect, url_for
from firebase_admin import firestore

db = firestore.client()
dbCollection = db.collection("employees")
login = Blueprint('login', __name__)


@login.route('/', methods=['GET'])
def show_form():
    return render_template('login.html')
    

@login.route('/verify', methods=['POST'])
def verify():
    # Get the JSON data from the request
    data = request.get_json()

    # Extract name and password from the JSON
    name = data.get('name')
    password = data.get('password')

    # Check for missing input
    if not name or not password:
        return jsonify({"error": "Invalid input"}), 400

    # Fetch user from Firestore by 'name'
    user_query = dbCollection.where('name', '==', name).stream()

    # Iterate over the query results to find the user
    for user_doc in user_query:
        user_data = user_doc.to_dict()

        # Check if the password matches
        if user_data.get('password') == password:
            return jsonify({"message": "Login successful", "user": user_data}), 200

    # If no match is found, return an error
    return jsonify({"error": "Invalid name or password"}), 401