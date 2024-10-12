from flask import Blueprint,request,jsonify, render_template
from firebase_admin import firestore

db = firestore.client()
user_Ref = db.collection("users")
userAPI = Blueprint("userAPI",__name__)

# render html
@userAPI.route('/form', methods=['GET'])
def show_form():
    return render_template('user.html')

@userAPI.route('/add', methods=['POST'])
def create_user():
    data = request.get_json()
    user_id = data.get('id')
    name = data.get('name')

    if user_id and name:
        user_Ref.document(user_id).set({'name': name,'id' : user_id})
        # user_Ref.document(user_id).set({'name': name})
        # user_Ref.document(user_id).set({'id' : user_id})
        return jsonify({"message": "User created", "id": user_id, "name": name}), 201
    else:
        return jsonify({"error": "Invalid input"}), 400

# GET: Retrieve a user by ID
@userAPI.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    user_doc = user_Ref.document(user_id).get()
    
    if user_doc.exists:
        return jsonify(user_doc.to_dict()), 200
    else:
        return jsonify({"error": "User not found"}), 404

# # DELETE: Delete a user by ID
# @userAPI.route('/<user_id>', methods=['DELETE'])
# def delete_user(user_id):
#     user_doc = user_Ref.document(user_id).get()
    
#     if user_doc.exists:
#         user_Ref.document(user_id).delete()
#         return jsonify({"message": "User deleted", "id": user_id}), 200
#     else:
#         return jsonify({"error": "User not found"}), 404

# # PATCH: Update a user's name by ID
# @userAPI.route('/<user_id>', methods=['PATCH'])
# def update_user(user_id):
#     data = request.get_json()
#     new_name = data.get('name')
    
#     if new_name:
#         user_doc = user_Ref.document(user_id).get()
#         if user_doc.exists:
#             user_Ref.document(user_id).update({'name': new_name})
#             return jsonify({"message": "User updated", "id": user_id, "new_name": new_name}), 200
#         else:
#             return jsonify({"error": "User not found"}), 404
#     else:
#         return jsonify({"error": "Invalid input"}), 400

# # Register the Blueprint
# # app.register_blueprint(userAPI, url_prefix='/api/user')
