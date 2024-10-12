import firebase_admin
from firebase_admin import credentials, firestore
import json

# Initialize Firebase Admin SDK
cred = credentials.Certificate('api/serviceAccountKey.json')
firebase_admin.initialize_app(cred)

# Connect to Firestore
db = firestore.client()

# Read the resumes JSON list from a file
with open('list_worker_resumes.json', 'r') as f:
    resumes_list = json.load(f)

# Save data to Firestore under "mentor_test" collection

for resume in resumes_list:
    # Use the "name" field as the document ID
    doc_ref = db.collection('mentor_test').document(resume['name'])
    doc_ref.set(resume)

print("Resumes have been uploaded to Firestore!")