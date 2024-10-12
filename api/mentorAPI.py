from flask import Blueprint,request,jsonify, render_template
from firebase_admin import firestore

db = firestore.client()
dbCollection = db.collection("mentors")
mentorAPI = Blueprint("mentorAPI",__name__)


@mentorAPI.route('/', methods=['GET'])
def showmentorpage():
    return render_template("mentors.html")


@mentorAPI.route('/getall', methods=['GET'])
def getallmentor():
    # Get the document for the user
    users = dbCollection.stream()
    all_users_data = []
    for user in users:
        if user.exists:
            # Get the 'skills' subcollection for each user
            skills_ref = dbCollection.document(user.id).collection("skills").stream()
            skills = [skill.id for skill in skills_ref]  # Get the document IDs for the skills

            # Combine the user's data and skills in the response
            user_data = user.to_dict()
            user_data['skills'] = skills
            
            all_users_data.append(user_data)
        
    if all_users_data:
        return jsonify(all_users_data), 200
    else:
        return jsonify({"error": "User not found"}), 404

@mentorAPI.route('/<name>', methods=['GET'])
def get_mentor(name):
    # Get the document for the user
    user_doc = dbCollection.document(name).get()
    
    if user_doc.exists:
        # Get the 'skills' subcollection for the user
        skills_ref = dbCollection.document(name).collection("skills").stream()
        skills = [skill.id for skill in skills_ref]  # Get the document IDs for the skills

        # Combine the user's data and skills in the response
        user_data = user_doc.to_dict()
        user_data['skills'] = skills
        
        return jsonify(user_data), 200
    else:
        return jsonify({"error": "User not found"}), 404
