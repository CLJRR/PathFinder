from flask import Blueprint,request,jsonify, render_template
from firebase_admin import firestore

db = firestore.client()
dbCollection = db.collection("employees")
employeeAPI = Blueprint("employeeAPI",__name__)

@employeeAPI.route('/',methods = ['GET'])
def show_form():
    return render_template('employeeDashboard.html')

@employeeAPI.route('/employees/<name>',methods = ['GET'])
def get_employee(name):
    try:
        employee_document = dbCollection.document(name).get()
        if name.exists:
            employee_data = employee_document.to_dict()
            return render_template('employeeDashboard.html',employee = employee_data)
        else:
            return jsonify({"error":"Employee not found"}), 404
    except Exception as e:
        return jsonify({"error": str(e)}),500
    

@employeeAPI.route('/employee/<name>/kpi', methods = ['GET'])
def display_kpi(name):
    kpi_ref= db.collection('kpi').document('base')
    kpi_doc = kpi_ref.get()
    if kpi_doc.exists:
        kpi_data = kpi_doc.to_dict()
        kpi_incidents = kpi_data.get('maxIncidents')

    employee_ref = db.collection('kpi').document(name)
    employee_doc = employee_ref.get()
    if employee_doc.exists:
        employee_data = employee_doc.todict()
        employee_incidents = employee_data.get("incidents")

    if employee_incidents >= kpi_incidents:
        return render_template('employee.html', risk = "High Risk")
    
    elif employee_incidents > kpi_incidents / 2:
        return render_template('employee.html', risk = "Medium Risk")
    
    elif employee_incidents > kpi_incidents / 3:
        return render_template('employee.html', risk = "Low Risk")
    
    else:
        return render_template('employee.html', risk = "No Risk")
        


    