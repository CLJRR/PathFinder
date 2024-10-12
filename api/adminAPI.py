from flask import Blueprint,request,jsonify, render_template
from firebase_admin import firestore

db = firestore.client()
dbEmployees = db.collection("employees")
dbCourses = db.collection("courses")
adminAPI = Blueprint("adminAPI",__name__)

@adminAPI.route('/', methods = ['GET'])
def show_form():
    return render_template('adminDashboard.html')


@adminAPI.route('/', methods = ['POST'])
def addToCourses():

    data = request.get_json()
    person_id = data.get('name')
    course_name = data.get('course_name')

    if not person_id or not course_name:
        return jsonify({"error": "Missing data"}), 400
    
    person_ref = dbEmployees(person_id)
    course_ref = dbCourses(course_name)

    try:
        def update_person(transaction):
            person_doc = person_ref.get(transaction=transaction)
            if person_doc.exists:
                person_data = person_doc.to_dict()
                courses = person_data.get('courses',[])
                courses.append(course_name)
                transaction.update(person_ref,{"courses":courses})
            else:
                transaction.set(person_ref,{"courses": [course_name]})

        def update_course(transaction):
            course_doc = course_ref.get(transaction=transaction)
            if course_doc.exists:
                course_data = course_doc.to_dict()
                people = course_data.get('people:',[])
                people.append(person_id)
                transaction.update(course_ref,{'people':people})
            else:
                transaction.set(course_ref,{'people':[person_id]})

        db.transaction(update_person)
        db.transaction(update_course)
        return jsonify({"message": "Course added to person successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}),500

# @adminAPI.route('/', methods = ['GET'])
# def viewCourse()
    
        



    



