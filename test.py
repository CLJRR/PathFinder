import firebase_admin
from firebase_admin import credentials,firestore

cred = credentials.Certificate("api/serviceAccountKey.json")
firebase_admin.initialize_app(cred)

db =firestore.client()
data ={
    'task':'test',
    's':'done'
}
ref = db.collection("tasks").document()
ref.set(data)